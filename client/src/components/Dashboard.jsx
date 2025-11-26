import React from 'react';
import { ShieldAlert, FileCode, Clock, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const MetricCard = ({ title, value, icon: Icon, color }) => (
  <div className="tech-card p-6 rounded-lg relative overflow-hidden group">
    <div className="relative z-10">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-2 rounded-md ${color.bg} text-white shadow-sm`}>
          <Icon className="w-5 h-5" />
        </div>
        <span className={`text-xs font-mono px-2 py-0.5 rounded-sm bg-opacity-10 ${color.bg} ${color.text}`}>
          +12%
        </span>
      </div>
      <p className="text-[var(--text-muted)] text-xs font-bold uppercase tracking-wider">{title}</p>
      <p className="text-3xl font-bold mt-1 text-[var(--text-main)] font-mono tracking-tight">{value}</p>
    </div>
  </div>
);

const Dashboard = ({ result }) => {
  if (!result) return null;

  // Process data for charts
  const severityCounts = result.issues.reduce((acc, issue) => {
    acc[issue.severity] = (acc[issue.severity] || 0) + 1;
    return acc;
  }, {});

  const severityData = [
    { name: 'Critical', count: severityCounts['Critical'] || 0, color: '#ef4444' },
    { name: 'High', count: severityCounts['High'] || 0, color: '#f97316' },
    { name: 'Medium', count: severityCounts['Medium'] || 0, color: '#eab308' },
    { name: 'Low', count: severityCounts['Low'] || 0, color: '#3b82f6' },
  ];

  const typeCounts = result.issues.reduce((acc, issue) => {
    acc[issue.vulnerability_type] = (acc[issue.vulnerability_type] || 0) + 1;
    return acc;
  }, {});

  const typeData = Object.keys(typeCounts).map((key, index) => ({
    name: key,
    value: typeCounts[key],
  }));

  const COLORS = ['#3b82f6', '#06b6d4', '#8b5cf6', '#10b981', '#f59e0b'];

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Severity Chart */}
        <div className="tech-card p-8 rounded-lg">
          <h3 className="text-sm font-bold mb-6 text-[var(--text-main)] flex items-center gap-2 uppercase tracking-wider">
            <Activity className="w-4 h-4 text-[var(--color-primary)]" />
            Issues by Severity
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" opacity={0.3} vertical={false} />
                <XAxis 
                  dataKey="name" 
                  stroke="var(--text-muted)" 
                  tick={{ fill: 'var(--text-muted)', fontSize: 11, fontFamily: 'JetBrains Mono' }} 
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis 
                  stroke="var(--text-muted)" 
                  tick={{ fill: 'var(--text-muted)', fontSize: 11, fontFamily: 'JetBrains Mono' }} 
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip 
                  cursor={{ fill: 'var(--bg-main)', opacity: 0.5 }}
                  contentStyle={{ 
                    backgroundColor: 'var(--bg-card)', 
                    borderColor: 'var(--border-color)', 
                    color: 'var(--text-main)',
                    borderRadius: '4px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    border: '1px solid var(--border-color)',
                  }}
                  itemStyle={{ color: 'var(--text-main)', fontFamily: 'JetBrains Mono', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[2, 2, 0, 0]} barSize={40}>
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Type Chart */}
        <div className="tech-card p-8 rounded-lg">
          <h3 className="text-sm font-bold mb-6 text-[var(--text-main)] flex items-center gap-2 uppercase tracking-wider">
            <ShieldAlert className="w-4 h-4 text-[var(--color-accent)]" />
            Top Vulnerabilities
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={typeData}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={110}
                  paddingAngle={2}
                  dataKey="value"
                  stroke="var(--bg-card)"
                  strokeWidth={2}
                >
                  {typeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                   contentStyle={{ 
                    backgroundColor: 'var(--bg-card)', 
                    borderColor: 'var(--border-color)', 
                    color: 'var(--text-main)',
                    borderRadius: '4px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    border: '1px solid var(--border-color)',
                  }}
                   itemStyle={{ color: 'var(--text-main)', fontFamily: 'JetBrains Mono', fontSize: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
