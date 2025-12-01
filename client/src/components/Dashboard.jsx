import React from 'react';
import axios from 'axios';
import { ShieldAlert, FileCode, Clock, Activity, Download } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const MetricCard = ({ title, value, icon: Icon, color }) => (
  <div className="modern-card p-6 flex items-center justify-between">
    <div>
      <p className="text-[var(--text-muted)] text-sm font-medium mb-1">{title}</p>
      <p className="text-3xl font-bold text-[var(--text-main)] tracking-tight">{value}</p>
    </div>
    <div className={`p-3 rounded-xl ${color.bg} text-[var(--bg-main)] shadow-sm`}>
      <Icon className="w-6 h-6" />
    </div>
  </div>
);

const Dashboard = ({ result }) => {
  if (!result) return null;

  const handleExport = async () => {
    if (!result.scan_id) {
      alert('Scan ID not found. Please save the scan first.');
      return;
    }
    try {
      const response = await axios.get(`http://localhost:8000/export/${result.scan_id}`, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `vulnora_report_${result.scan_id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Export failed:', err);
      alert('Failed to export report');
    }
  };

  // Process data for charts
  const severityCounts = result.issues.reduce((acc, issue) => {
    acc[issue.severity] = (acc[issue.severity] || 0) + 1;
    return acc;
  }, {});

  const severityData = [
    { name: 'Critical', count: severityCounts['Critical'] || 0, color: '#000000' }, // Black
    { name: 'High', count: severityCounts['High'] || 0, color: '#333333' }, // Dark Gray
    { name: 'Medium', count: severityCounts['Medium'] || 0, color: '#666666' }, // Medium Gray
    { name: 'Low', count: severityCounts['Low'] || 0, color: '#999999' }, // Light Gray
  ];

  const typeCounts = result.issues.reduce((acc, issue) => {
    acc[issue.vulnerability_type] = (acc[issue.vulnerability_type] || 0) + 1;
    return acc;
  }, {});

  const typeData = Object.keys(typeCounts).map((key, index) => ({
    name: key,
    value: typeCounts[key],
  }));

  // Monochrome theme colors for charts
  const COLORS = ['#000000', '#333333', '#666666', '#999999', '#CCCCCC'];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-[var(--text-main)]">Scan Dashboard</h2>
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 bg-[var(--color-primary)] text-[var(--bg-main)] rounded-lg hover:bg-[var(--color-primary-hover)] transition-colors"
        >
          <Download className="w-4 h-4" />
          Export PDF
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Issues"
          value={result.issues.length}
          icon={ShieldAlert}
          color={{ bg: 'bg-[var(--color-primary)]', text: 'text-red-500' }} // Keep red for issues
        />
        <MetricCard
          title="Smell Score"
          value={result.smell_score}
          icon={Activity}
          color={{ bg: 'bg-[var(--color-primary)]', text: 'text-[var(--text-main)]' }} // Use theme accent
        />
        <MetricCard
          title="Files Scanned"
          value={result.files_scanned}
          icon={FileCode}
          color={{ bg: 'bg-[var(--color-primary)]', text: 'text-white' }} // Use theme primary
        />
        <MetricCard
          title="Scan Duration"
          value={`${result.scan_duration}s`}
          icon={Clock}
          color={{ bg: 'bg-[var(--color-primary)]', text: 'text-white' }} // Use theme secondary
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
