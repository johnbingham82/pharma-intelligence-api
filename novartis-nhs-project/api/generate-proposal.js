// API: Generate Proposal
require('dotenv').config();
const fetch = require('node-fetch');

const CONFIG = {
    CLAUDE_API_KEY: process.env.CLAUDE_API_KEY,
    CLAUDE_MODEL: process.env.CLAUDE_MODEL || 'claude-sonnet-4-5-20250929',
    CLAUDE_API_URL: 'https://api.anthropic.com/v1/messages'
};

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

module.exports = async (req, res) => {
    // Set no-cache headers
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { userContext, relevantProjects, structuredContext } = req.body;

        if (!userContext || !relevantProjects) {
            return res.status(400).json({
                error: 'Missing required fields',
                required: ['userContext', 'relevantProjects']
            });
        }

        const claudeRequest = {
            model: CONFIG.CLAUDE_MODEL,
            max_tokens: 4000,
            temperature: 0.8,
            system: buildSystemPrompt(),
            messages: [
                {
                    role: 'user',
                    content: buildUserPrompt(userContext, relevantProjects, structuredContext)
                }
            ]
        };

        console.log('[API] Generating proposal with structured context:', {
            hasOrgName: !!structuredContext?.organizationName,
            orgName: structuredContext?.organizationName
        });

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
            console.error('[API Error]', response.status, errorText);
            return res.status(response.status).json({
                error: 'Claude API error',
                status: response.status
            });
        }

        const data = await response.json();
        const content = data.content[0].text;
        const cleanContent = content.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
        
        let proposalData;
        try {
            proposalData = JSON.parse(cleanContent);
        } catch (parseError) {
            console.error('[Parse Error] Failed to parse Claude response');
            return res.status(500).json({
                error: 'Invalid response format from AI'
            });
        }

        if (!proposalData.hookStatement || !proposalData.projectScenario) {
            return res.status(500).json({
                error: 'Invalid proposal structure'
            });
        }

        console.log('[Success] Proposal generated');

        res.json({
            success: true,
            proposal: proposalData,
            metadata: {
                model: CONFIG.CLAUDE_MODEL,
                matchedProjects: relevantProjects.length,
                timestamp: new Date().toISOString()
            }
        });

    } catch (error) {
        console.error('[Server Error]', error);
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
};
