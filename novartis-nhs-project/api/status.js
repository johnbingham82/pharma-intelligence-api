// API: Status Check
module.exports = (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    res.json({
        status: 'operational',
        claudeApiConfigured: !!process.env.CLAUDE_API_KEY,
        model: process.env.CLAUDE_MODEL || 'claude-sonnet-4-5-20250929',
        version: '2.1.1',
        timestamp: new Date().toISOString()
    });
};
