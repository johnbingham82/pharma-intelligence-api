// ============================================
// NOVARTIS CWP BACKEND API
// Secure server for Claude API integration
// ============================================

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
    CLAUDE_API_KEY: process.env.CLAUDE_API_KEY,
    CLAUDE_MODEL: process.env.CLAUDE_MODEL || 'claude-sonnet-4-5-20250929',
    CLAUDE_API_URL: 'https://api.anthropic.com/v1/messages',
    ALLOWED_ORIGINS: process.env.ALLOWED_ORIGINS ? 
        process.env.ALLOWED_ORIGINS.split(',') : 
        ['http://localhost:3000', 'http://localhost:8080'],
    MAX_REQUESTS_PER_MINUTE: parseInt(process.env.MAX_REQUESTS_PER_MINUTE || '20'),
    NODE_ENV: process.env.NODE_ENV || 'development'
};

// Validate required environment variables
if (!CONFIG.CLAUDE_API_KEY) {
    console.error('❌ ERROR: CLAUDE_API_KEY not set in environment variables');
    console.error('Please create a .env file with your API key');
    process.exit(1);
}

// ============================================
// MIDDLEWARE
// ============================================

// Security headers
app.use(helmet());

// CORS configuration
const corsOptions = {
    origin: function (origin, callback) {
        // Allow requests with no origin (like mobile apps or curl)
        if (!origin) return callback(null, true);
        
        if (CONFIG.ALLOWED_ORIGINS.indexOf(origin) !== -1 || CONFIG.NODE_ENV === 'development') {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    credentials: true,
    optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// Parse JSON bodies
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: CONFIG.MAX_REQUESTS_PER_MINUTE,
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
});
app.use('/api/', limiter);

// Request logging
app.use((req, res, next) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} ${req.path}`);
    next();
});

// ============================================
// ROUTES
// ============================================

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        environment: CONFIG.NODE_ENV,
        version: '1.0.0'
    });
});

// API status check
app.get('/api/status', (req, res) => {
    res.json({
        status: 'operational',
        claudeApiConfigured: !!CONFIG.CLAUDE_API_KEY,
        model: CONFIG.CLAUDE_MODEL,
        rateLimit: `${CONFIG.MAX_REQUESTS_PER_MINUTE} requests/minute`,
        timestamp: new Date().toISOString()
    });
});

// Main proposal generation endpoint
app.post('/api/generate-proposal', async (req, res) => {
    const startTime = Date.now();
    
    // CRITICAL: Prevent all caching - each proposal must be unique
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    
    try {
        const { userContext, relevantProjects, systemPrompt, userPrompt, structuredContext } = req.body;

        // Validate request
        if (!userContext || !relevantProjects) {
            return res.status(400).json({
                error: 'Missing required fields',
                required: ['userContext', 'relevantProjects']
            });
        }

        // Build the Claude API request
        const claudeRequest = {
            model: CONFIG.CLAUDE_MODEL,
            max_tokens: 4000,
            temperature: 0.8,
            system: systemPrompt || buildSystemPrompt(),
            messages: [
                {
                    role: 'user',
                    content: userPrompt || buildUserPrompt(userContext, relevantProjects, structuredContext)
                }
            ]
        };

        // Call Claude API
        console.log(`[API Call] Generating proposal with ${relevantProjects.length} matched projects`);
        
        const response = await fetch(CONFIG.CLAUDE_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': CONFIG.CLAUDE_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify(claudeRequest)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`[API Error] ${response.status}: ${errorText}`);
            
            return res.status(response.status).json({
                error: 'Claude API error',
                status: response.status,
                message: response.statusText
            });
        }

        const data = await response.json();
        const generationTime = Date.now() - startTime;

        // Extract and parse the proposal
        const content = data.content[0].text;
        const cleanContent = content.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
        
        let proposalData;
        try {
            proposalData = JSON.parse(cleanContent);
        } catch (parseError) {
            console.error('[Parse Error] Failed to parse Claude response as JSON');
            return res.status(500).json({
                error: 'Invalid response format from AI',
                details: 'Response was not valid JSON'
            });
        }

        // Validate proposal structure
        if (!proposalData.hookStatement || !proposalData.projectScenario) {
            console.error('[Validation Error] Missing required proposal fields');
            return res.status(500).json({
                error: 'Invalid proposal structure',
                details: 'Missing required fields'
            });
        }

        // Log success metrics
        console.log(`[Success] Proposal generated in ${generationTime}ms`);
        console.log(`[Tokens] Input: ~${Math.round(claudeRequest.messages[0].content.length / 4)}, Output: ~${Math.round(content.length / 4)}`);

        // Return the proposal
        res.json({
            success: true,
            proposal: proposalData,
            metadata: {
                generationTime,
                model: CONFIG.CLAUDE_MODEL,
                matchedProjects: relevantProjects.length,
                timestamp: new Date().toISOString()
            }
        });

    } catch (error) {
        console.error('[Server Error]', error);
        console.error('[Stack]', error.stack);
        res.status(500).json({
            error: 'Internal server error',
            message: error.message,
            stack: CONFIG.NODE_ENV === 'development' ? error.stack : undefined
        });
    }
});

// Email submission endpoint (for future integration with CRM)
app.post('/api/submit-contact', async (req, res) => {
    try {
        const { name, email, organization, role, consent } = req.body;

        // Validate required fields
        if (!name || !email || !organization || !role || !consent) {
            return res.status(400).json({
                error: 'Missing required fields',
                required: ['name', 'email', 'organization', 'role', 'consent']
            });
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json({
                error: 'Invalid email format'
            });
        }

        // Log the submission (in production, save to database/CRM)
        console.log('[Contact Submission]', {
            name,
            email,
            organization,
            role,
            timestamp: new Date().toISOString()
        });

        // TODO: Integrate with your CRM system here
        // await saveToCRM({ name, email, organization, role });
        
        // TODO: Send email with proposal
        // await sendEmail(email, proposalPDF);

        res.json({
            success: true,
            message: 'Contact information received',
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('[Contact Submission Error]', error);
        res.status(500).json({
            error: 'Failed to process submission'
        });
    }
});

// ============================================
// HELPER FUNCTIONS
// ============================================

function buildSystemPrompt() {
    return `You are an expert healthcare transformation consultant specialising in NHS collaborative working projects. Your role is to create INSPIRATIONAL, narrative-driven proposals that show stakeholders how their challenges can be solved through partnership with Novartis.

CRITICAL PARTNERSHIP APPROACH:
**NOVARTIS PROVIDES COLLABORATIVE SOLUTIONS - NOT FUNDING**
Solutions must focus on:
- Deploying specialist WORKFORCE (e.g., clinical nurse specialists, pharmacists, registrars)
- Sharing clinical EXPERTISE and best practices
- Implementing proven care PATHWAYS and service models
- Providing TECHNOLOGY and digital tools
- Building CAPACITY through training and support
- Optimising PROCESSES and patient flow

**NEVER suggest:**
- Direct financial contributions
- Grants or funding
- "Paying for" services
- Budget supplements

**INSTEAD emphasise:**
- "Partnership to deploy a specialist nurse..."
- "Collaborative working to implement a proven pathway..."
- "Sharing expertise to build capacity..."
- "Working together to optimise your service..."

CRITICAL INSTRUCTIONS:
- Write in BRITISH ENGLISH spelling throughout (organisation, personalise, analyse, etc.)
- Write in an INSPIRATIONAL, STORYTELLING style, NOT a formal executive summary
- Use "imagine this", "picture this", "envision" language to paint vivid scenarios
- Make the transformation feel ACHIEVABLE and REAL
- Include SPECIFIC metrics (e.g., "60-80% reduction") based on real CWP outcomes
- Be EMPATHETIC to NHS pressures and constraints
- Focus on PARTNERSHIP language, not sales pitch
- Keep tone OPTIMISTIC but REALISTIC

OUTPUT FORMAT (JSON):
{
  "hookStatement": "Opening 'Imagine this...' statement personalised to their challenge",
  "visionStatement": "One-sentence transformation vision",
  "challengeStory": "Empathetic 2-3 sentence acknowledgement of their reality",
  "opportunityStory": "2-3 sentences about what collaborative working unlocks",
  "exampleReference": "One sentence about a similar organisation's success",
  "projectScenario": "Vivid 3-4 sentence description of how this could work for them",
  "timelineNarrative": "One sentence describing progressive 12-month transformation",
  "patientStats": ["stat 1", "stat 2", "stat 3", "stat 4"],
  "organisationStats": ["stat 1", "stat 2", "stat 3", "stat 4"],
  "systemStats": ["stat 1", "stat 2", "stat 3", "stat 4"],
  "principleDescriptions": {
    "proven": "Brief description of why it's proven",
    "realistic": "Brief description of NHS fit",
    "partnership": "Brief description of partnership approach",
    "sustainable": "Brief description of sustainability"
  },
  "nextStepsStory": "2-3 sentences inviting conversation without pressure",
  "closingCTA": "One compelling sentence question to end with"
}`;
}

function buildUserPrompt(userContext, relevantProjects, structuredContext = null) {
    const projectsText = relevantProjects.map((p, idx) => `
${idx + 1}. ${p.name}
   Focus: ${p.focus}
   Problem: ${p.problem}
   Solution: ${p.solution}
   Benefits: ${Array.isArray(p.benefits) ? p.benefits.join(', ') : p.benefits}
`).join('\n');

    // Build rich context from structured conversation if available
    let contextSection = `USER CONTEXT (their challenge):
${userContext}`;

    if (structuredContext && structuredContext.challenge) {
        const orgNameSection = structuredContext.organizationName 
            ? `ORGANIZATION: ${structuredContext.organizationName}\n\n` 
            : '';
        
        contextSection = `DETAILED USER CONTEXT:

${orgNameSection}PRIMARY CHALLENGE:
${structuredContext.challenge}

SPECIFIC REQUIREMENTS & METRICS:
${structuredContext.specifics}

CONSTRAINTS & CONSIDERATIONS:
${structuredContext.constraints}

COMPLETE CONTEXT:
${structuredContext.fullContext}`;
    }

    return `${contextSection}

MATCHED COLLABORATIVE WORKING PROJECTS (use as inspiration):
${projectsText}

TASK:
Generate a HIGHLY PERSONALISED INSPIRATIONAL transformation story that addresses their SPECIFIC situation. 

CRITICAL - SOLUTION APPROACH:
Focus solutions on COLLABORATIVE WORKING (deploying specialist roles, sharing expertise, implementing pathways, providing technology).
NEVER mention funding, grants, or financial contributions - this is about partnership, not money.

CRITICAL - PERSONALIZATION REQUIREMENTS:
- **IF organization name is provided, USE IT throughout the proposal** (e.g., "Imagine this at [Trust Name]", "For [Trust Name], this means...")
- Reference their SPECIFIC metrics, timeframes, and constraints mentioned
- Address their EXACT challenges (not generic problems)
- Tailor solutions to their stated requirements
- Use their terminology and context throughout
- Make it feel like it was written specifically for them, not a template

REMEMBER:
- Use BRITISH ENGLISH spelling throughout (organisation, realise, analyse, etc.)
- Paint a vivid picture using THEIR specific situation
- Show specific, measurable outcomes relevant to THEIR metrics
- Address THEIR stated constraints and considerations
- Make it feel achievable given THEIR context
- Use warm, inviting language for next steps
- Include specific stats based on real CWP outcomes that match THEIR scale
- Solutions focus on PEOPLE, EXPERTISE, PATHWAYS, TECHNOLOGY - not funding

Return ONLY valid JSON with no markdown formatting or code fences.`;
}

// ============================================
// ERROR HANDLING
// ============================================

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        error: 'Endpoint not found',
        availableEndpoints: [
            'GET /health',
            'GET /api/status',
            'POST /api/generate-proposal',
            'POST /api/submit-contact'
        ]
    });
});

// Global error handler
app.use((err, req, res, next) => {
    console.error('[Global Error]', err);
    res.status(500).json({
        error: 'Internal server error',
        message: CONFIG.NODE_ENV === 'development' ? err.message : 'An error occurred'
    });
});

// ============================================
// START SERVER
// ============================================

// Only start server if running directly (not when imported as module for Vercel)
if (require.main === module) {
    app.listen(PORT, () => {
        console.log('\n🚀 Novartis CWP Backend API');
        console.log('================================');
        console.log(`✅ Server running on port ${PORT}`);
        console.log(`✅ Environment: ${CONFIG.NODE_ENV}`);
        console.log(`✅ Claude API: Configured`);
        console.log(`✅ Model: ${CONFIG.CLAUDE_MODEL}`);
        console.log(`✅ Rate limit: ${CONFIG.MAX_REQUESTS_PER_MINUTE} requests/minute`);
        console.log('\nEndpoints:');
        console.log(`  GET  http://localhost:${PORT}/health`);
        console.log(`  GET  http://localhost:${PORT}/api/status`);
        console.log(`  POST http://localhost:${PORT}/api/generate-proposal`);
        console.log(`  POST http://localhost:${PORT}/api/submit-contact`);
        console.log('\n💡 Tip: Test with: curl http://localhost:' + PORT + '/health\n');
    });

    // Graceful shutdown
    process.on('SIGTERM', () => {
        console.log('SIGTERM received, shutting down gracefully...');
        process.exit(0);
    });

    process.on('SIGINT', () => {
        console.log('\nSIGINT received, shutting down gracefully...');
        process.exit(0);
    });
}

// Export the app for Vercel serverless deployment
module.exports = app;
