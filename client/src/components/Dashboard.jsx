import React from 'react';
import { ShieldAlert, FileCode, Clock, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const MetricCard = ({ title, value, icon: Icon, color }) => (
  <div className="modern-card p-6 flex items-center justify-between">
    <div>
      <p className="text-[var(--text-muted)] text-sm font-medium mb-1">{title}</p>
      <p className="text-3xl font-bold text-[var(--text-main)] tracking-tight">{value}</p>
    </div>
    <div className={`p-3 rounded-xl ${color.bg} text-white shadow-sm`}>
      <Icon className="w-6 h-6" />
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

  const COLORS = ['#6366f1', '#ec4899', '#8b5cf6', '#14b8a6', '#f43f5e'];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Severity Chart */}
        <div className="modern-card p-6">
          <h3 className="text-base font-semibold mb-6 text-[var(--text-main)] flex items-center gap-2">
            <Activity className="w-4 h-4 text-[var(--text-muted)]" />
            Issues by Severity
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  stroke="var(--text-muted)" 
                  tick={{ fill: 'var(--text-muted)', fontSize: 12 }} 
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis 
                  stroke="var(--text-muted)" 
                  tick={{ fill: 'var(--text-muted)', fontSize: 12 }} 
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip 
                  cursor={{ fill: 'var(--bg-main)', opacity: 0.5 }}
                  contentStyle={{ 
                    backgroundColor: 'var(--bg-card)', 
                    borderColor: 'var(--border-color)', 
                    color: 'var(--text-main)',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  }}
                  itemStyle={{ color: 'var(--text-main)' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} barSize={32}>
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Type Chart */}
        <div className="modern-card p-6">
          <h3 className="text-base font-semibold mb-6 text-[var(--text-main)] flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-[var(--text-muted)]" />
            Top Vulnerabilities
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={typeData}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={100}
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
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  }}
                   itemStyle={{ color: 'var(--text-main)' }}
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
