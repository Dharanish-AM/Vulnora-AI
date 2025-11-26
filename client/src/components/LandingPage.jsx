import React from 'react';
import { Shield, Zap, FileText, ArrowRight } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="modern-card p-6 hover:border-[var(--color-primary)] transition-colors group">
    <div className="w-12 h-12 rounded-lg bg-[var(--color-primary)]/10 flex items-center justify-center mb-4 group-hover:bg-[var(--color-primary)] transition-colors">
      <Icon className="w-6 h-6 text-[var(--color-primary)] group-hover:text-white transition-colors" />
    </div>
    <h3 className="text-lg font-semibold text-[var(--text-main)] mb-2">{title}</h3>
    <p className="text-sm text-[var(--text-muted)] leading-relaxed">{description}</p>
  </div>
);

const LandingPage = ({ onStart }) => {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center text-center space-y-16 animate-in fade-in duration-700">
      {/* Hero Section */}
      <div className="space-y-6 max-w-3xl mx-auto px-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] text-xs font-medium mb-4">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-primary)] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-[var(--color-primary)]"></span>
          </span>
          v2.0 Now Available
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold text-[var(--text-main)] tracking-tight">
          See the <span className="text-[var(--color-primary)]">Unseen</span>
        </h1>
        
        <p className="text-lg md:text-xl text-[var(--text-muted)] max-w-2xl mx-auto leading-relaxed">
          Advanced AI-powered security analysis for your code. Detect vulnerabilities, 
          understand risks, and fix issues before they deploy.
        </p>
        
        <div className="pt-4">
          <button
            onClick={onStart}
            className="group relative inline-flex items-center justify-center px-8 py-4 font-semibold text-white transition-all duration-200 bg-[var(--color-primary)] rounded-full hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600"
          >
            Get Started
            <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            <div className="absolute inset-0 rounded-full ring-2 ring-white/20 group-hover:ring-white/40 transition-all" />
          </button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto px-4 w-full">
        <FeatureCard
          icon={Shield}
          title="Deep Security Analysis"
          description="Identify critical vulnerabilities including SQL Injection, XSS, and more using advanced static analysis rules."
        />
        <FeatureCard
          icon={Zap}
          title="AI-Powered Insights"
          description="Leverage LLMs to understand the context of vulnerabilities and generate intelligent remediation suggestions."
        />
        <FeatureCard
          icon={FileText}
          title="Comprehensive Reports"
          description="Get detailed breakdowns of security posture, code smell scores, and actionable fix recommendations."
        />
      </div>
    </div>
  );
};

export default LandingPage;
