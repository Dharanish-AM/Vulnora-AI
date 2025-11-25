import React from 'react';
import { ShieldAlert, FileCode, Clock, Activity } from 'lucide-react';

const MetricCard = ({ title, value, icon: Icon, color }) => (
  <div className="bg-card p-6 rounded-xl shadow-lg border border-slate-700">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-slate-400 text-sm">{title}</p>
        <p className="text-3xl font-bold mt-1">{value}</p>
      </div>
      <div className={`p-3 rounded-lg bg-opacity-10 ${color.bg}`}>
        <Icon className={`w-6 h-6 ${color.text}`} />
      </div>
    </div>
  </div>
);

const Dashboard = ({ result }) => {
  if (!result) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <MetricCard
        title="Total Issues"
        value={result.issues.length}
        icon={ShieldAlert}
        color={{ bg: 'bg-red-500', text: 'text-red-500' }}
      />
      <MetricCard
        title="Smell Score"
        value={result.smell_score}
        icon={Activity}
        color={{ bg: 'bg-yellow-500', text: 'text-yellow-500' }}
      />
      <MetricCard
        title="Files Scanned"
        value={result.files_scanned}
        icon={FileCode}
        color={{ bg: 'bg-blue-500', text: 'text-blue-500' }}
      />
      <MetricCard
        title="Scan Duration"
        value={`${result.scan_duration}s`}
        icon={Clock}
        color={{ bg: 'bg-green-500', text: 'text-green-500' }}
      />
    </div>
  );
};

export default Dashboard;
