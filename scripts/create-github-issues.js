const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Try to load .env file if running locally
try {
  require('dotenv').config();
} catch (error) {
  // dotenv not available or .env file doesn't exist - that's fine for GitHub Actions
  console.log('Running without .env file (likely in GitHub Actions)');
}

// Configuration - use environment variables or defaults
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'beslagicadin';
const GITHUB_REPO = process.env.GITHUB_REPO || 'polyglot-dev-toolkit';
const SONAR_PROJECT_KEY = process.env.SONAR_PROJECT_KEY || 'beslagicadin_polyglot-dev-toolkit';

class SonarQubeGitHubIssueCreator {
  constructor(githubToken, sonarToken) {
    this.githubToken = githubToken;
    this.sonarToken = sonarToken;
    this.githubApi = axios.create({
      baseURL: 'https://api.github.com',
      headers: {
        'Authorization': `token ${githubToken}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    this.sonarApi = axios.create({
      baseURL: 'https://sonarcloud.io/api',
      headers: {
        'Authorization': `Bearer ${sonarToken}`
      }
    });
  }

  async getSonarQubeIssues() {
    try {
      const response = await this.sonarApi.get('/issues/search', {
        params: {
          componentKeys: SONAR_PROJECT_KEY,
          resolved: 'false',
          severities: 'BLOCKER,CRITICAL,MAJOR',
          types: 'BUG,VULNERABILITY,SECURITY_HOTSPOT'
        }
      });
      return response.data.issues;
    } catch (error) {
      console.error('Error fetching SonarQube issues:', error.message);
      return [];
    }
  }

  async getExistingGitHubIssues() {
    try {
      const response = await this.githubApi.get(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues`, {
        params: {
          labels: 'sonarqube',
          state: 'open'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching GitHub issues:', error.message);
      return [];
    }
  }

  async createGitHubIssue(sonarIssue) {
    const title = `[SonarQube] ${sonarIssue.type}: ${sonarIssue.message}`;
    const body = this.generateIssueBody(sonarIssue);
    const labels = this.generateLabels(sonarIssue);

    try {
      const response = await this.githubApi.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues`, {
        title,
        body,
        labels
      });
      console.log(`✅ Created GitHub issue: ${response.data.html_url}`);
      return response.data;
    } catch (error) {
      console.error(`❌ Error creating GitHub issue: ${error.message}`);
      return null;
    }
  }

  generateIssueBody(sonarIssue) {
    return `## SonarQube Issue Details

**Type:** ${sonarIssue.type}
**Severity:** ${sonarIssue.severity}
**Rule:** ${sonarIssue.rule}
**Component:** ${sonarIssue.component}

### Description
${sonarIssue.message}

### Location
- **File:** \`${sonarIssue.component.replace(SONAR_PROJECT_KEY + ':', '')}\`
- **Line:** ${sonarIssue.line || 'N/A'}

### SonarQube Link
[View in SonarCloud](https://sonarcloud.io/project/issues?id=${SONAR_PROJECT_KEY}&issues=${sonarIssue.key}&open=${sonarIssue.key})

---
*This issue was automatically created from SonarQube analysis results.*
*Issue Key: \`${sonarIssue.key}\`*`;
  }

  generateLabels(sonarIssue) {
    const labels = ['sonarqube'];
    
    // Add severity label
    labels.push(`severity:${sonarIssue.severity.toLowerCase()}`);
    
    // Add type label
    switch (sonarIssue.type) {
      case 'BUG':
        labels.push('bug');
        break;
      case 'VULNERABILITY':
        labels.push('security', 'vulnerability');
        break;
      case 'SECURITY_HOTSPOT':
        labels.push('security', 'security-hotspot');
        break;
      case 'CODE_SMELL':
        labels.push('code-quality');
        break;
    }

    return labels;
  }

  async syncIssues() {
    console.log('🔄 Starting SonarQube to GitHub Issues sync...');
    
    const [sonarIssues, githubIssues] = await Promise.all([
      this.getSonarQubeIssues(),
      this.getExistingGitHubIssues()
    ]);

    console.log(`📊 Found ${sonarIssues.length} SonarQube issues and ${githubIssues.length} existing GitHub issues`);

    // Get SonarQube issue keys that already have GitHub issues
    const existingIssueKeys = githubIssues
      .map(issue => {
        const match = issue.body.match(/Issue Key: `([^`]+)`/);
        return match ? match[1] : null;
      })
      .filter(Boolean);

    // Create GitHub issues for new SonarQube issues
    const newSonarIssues = sonarIssues.filter(issue => !existingIssueKeys.includes(issue.key));
    
    console.log(`📝 Creating ${newSonarIssues.length} new GitHub issues...`);

    for (const sonarIssue of newSonarIssues) {
      await this.createGitHubIssue(sonarIssue);
      // Add a small delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    console.log('✅ Sync completed!');
  }
}

// CLI usage
async function main() {
  const githubToken = process.env.GITHUB_TOKEN;
  const sonarToken = process.env.SONAR_TOKEN;

  if (!githubToken) {
    console.error('❌ GITHUB_TOKEN environment variable is required');
    process.exit(1);
  }

  if (!sonarToken) {
    console.error('❌ SONAR_TOKEN environment variable is required');
    process.exit(1);
  }

  const issueCreator = new SonarQubeGitHubIssueCreator(githubToken, sonarToken);
  await issueCreator.syncIssues();
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Script failed:', error.message);
    process.exit(1);
  });
}

module.exports = SonarQubeGitHubIssueCreator;
