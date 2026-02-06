// Enhanced Conversation Logic for Novartis CWP Generator
// This replaces the static question flow with adaptive, context-aware questioning

const extractOrganizationInfo = (text) => {
    // Extract organization name patterns
    const patterns = [
        /(?:at|from|with|for)\s+([A-Z][a-zA-Z\s&'-]+(?:NHS Trust|Trust|ICS|ICB|Hospital|Health Board|Healthcare|CCG))/gi,
        /([A-Z][a-zA-Z\s&'-]+(?:NHS Trust|Trust|ICS|ICB|Hospital|Health Board|Healthcare|CCG))/gi,
        /(?:we're|we are)\s+([A-Z][a-zA-Z\s&'-]+)/gi
    ];
    
    for (const pattern of patterns) {
        const matches = [...text.matchAll(pattern)];
        if (matches.length > 0) {
            return matches[0][1].trim();
        }
    }
    
    return null;
};

const analyzeProvidedInfo = (messages) => {
    const fullText = messages.map(m => m.content).join(' ').toLowerCase();
    
    return {
        hasOrganization: extractOrganizationInfo(messages.map(m => m.content).join(' ')) !== null,
        hasMetrics: /\d+%|\d+ (patients?|hours?|days?|weeks?|months?)|\d+k|waiting time|capacity|throughput/i.test(fullText),
        hasTimeline: /month|year|quarter|week|urgent|asap|by \d+/i.test(fullText),
        hasConstraints: /budget|staff|resource|capacity|infrastructure|technology|limited|challenge/i.test(fullText),
        hasSpecificGoal: /reduce|increase|improve|achieve|target|goal|outcome/i.test(fullText),
        hasScope: /ward|department|trust-wide|system-wide|pathway|service|clinic/i.test(fullText),
        hasProblemArea: /waiting|backlog|capacity|outcome|readmission|discharge|access|quality/i.test(fullText)
    };
};

const generateAdaptiveQuestion = (userMessages, messageCount) => {
    const allText = userMessages.join('\n\n');
    const orgName = extractOrganizationInfo(allText);
    const provided = analyzeProvidedInfo(userMessages.map(content => ({ content })));
    
    // First follow-up - ask for what's missing from initial description
    if (messageCount === 1) {
        const missingElements = [];
        
        if (!provided.hasOrganization) {
            return "Thanks for sharing that. Before we dive into solutions, could you tell me which Trust or ICS you're working with? This will help me tailor the proposal specifically for your organization.";
        }
        
        let question = `Thanks for sharing that${orgName ? `, ${orgName}` : ''}. `;
        
        if (!provided.hasMetrics) {
            missingElements.push("• What are your current numbers? (e.g., waiting times, patient volumes, capacity utilization)");
        }
        
        if (!provided.hasSpecificGoal) {
            missingElements.push("• What specific improvement would you like to achieve?");
        }
        
        if (!provided.hasTimeline) {
            missingElements.push("• What's your timeframe for seeing results?");
        }
        
        if (missingElements.length > 0) {
            question += "To create the most relevant solution, could you tell me:\n\n" + missingElements.join('\n');
        } else {
            // Everything provided - ask about constraints
            question += "That's comprehensive. What are your main constraints or considerations? For example, workforce challenges, infrastructure needs, or operational factors.";
        }
        
        return question;
    }
    
    // Second follow-up - fill remaining gaps
    if (messageCount === 2) {
        const stillMissing = [];
        
        if (!provided.hasConstraints) {
            stillMissing.push("• What constraints or challenges need to be considered?");
        }
        
        if (!provided.hasScope) {
            stillMissing.push("• What's the scope? (e.g., single department, trust-wide, pathway)");
        }
        
        if (!provided.hasMetrics && !provided.hasSpecificGoal) {
            stillMissing.push("• What does success look like in measurable terms?");
        }
        
        if (stillMissing.length > 0) {
            return `That's helpful${orgName ? `, ${orgName}` : ''}. A couple more things:\n\n` + stillMissing.join('\n');
        } else {
            // All info gathered
            return `Perfect! I have everything I need${orgName ? ` to create a tailored proposal for ${orgName}` : ''}. Let me put together something specific to your situation...`;
        }
    }
    
    // Third message - should always generate
    return `Excellent${orgName ? `, ${orgName}` : ''}. I have a clear picture now. Let me create a highly personalised proposal that addresses your specific situation...`;
};

const buildStructuredContext = (userMessages) => {
    const allText = userMessages.join('\n\n');
    const orgName = extractOrganizationInfo(allText);
    const provided = analyzeProvidedInfo(userMessages.map(content => ({ content })));
    
    return {
        organizationName: orgName,
        challenge: userMessages[0],
        specifics: userMessages[1] || '',
        constraints: userMessages[2] || '',
        fullContext: allText,
        hasMetrics: provided.hasMetrics,
        hasTimeline: provided.hasTimeline,
        hasConstraints: provided.hasConstraints,
        analyzedInfo: provided
    };
};

// Export for use in main app
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        extractOrganizationInfo,
        analyzeProvidedInfo,
        generateAdaptiveQuestion,
        buildStructuredContext
    };
}
