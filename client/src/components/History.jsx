import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Calendar, Clock, AlertTriangle, Download, ArrowRight, Loader2 } from 'lucide-react';

const History = ({ onLoadScan }) => {
    const [scans, setScans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await axios.get('http://localhost:8000/history');
            setScans(response.data);
            setLoading(false);
        } catch (err) {
            setError('Failed to load history');
            setLoading(false);
        }
    };

    const handleExport = async (scanId) => {
        try {
            const response = await axios.get(`http://localhost:8000/export/${scanId}`, {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `vulnora_report_${scanId}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.error('Export failed:', err);
            alert('Failed to export report');
        }
    };

    const handleLoad = async (scanId) => {
        try {
            const response = await axios.get(`http://localhost:8000/history/${scanId}`);
            onLoadScan(response.data);
        } catch (err) {
            console.error('Failed to load scan:', err);
            alert('Failed to load scan details');
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <Loader2 className="w-8 h-8 animate-spin text-[var(--color-primary)]" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center text-red-500 p-8">
                <AlertTriangle className="w-12 h-12 mx-auto mb-4" />
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto p-6">
            <h2 className="text-3xl font-bold mb-8 text-[var(--text-main)] flex items-center gap-3">
                <Clock className="w-8 h-8" />
                Scan History
            </h2>

            <div className="bg-[var(--bg-card)] rounded-xl shadow-lg overflow-hidden border border-[var(--border-color)]">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-[var(--bg-main)] border-b border-[var(--border-color)]">
                            <tr>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-[var(--text-muted)]">Date</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-[var(--text-muted)]">Project</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-[var(--text-muted)]">Smell Score</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-[var(--text-muted)]">Files</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-[var(--text-muted)]">Duration</th>
                                <th className="px-6 py-4 text-right text-sm font-semibold text-[var(--text-muted)]">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-[var(--border-color)]">
                            {scans.length === 0 ? (
                                <tr>
                                    <td colSpan="6" className="px-6 py-12 text-center text-[var(--text-muted)]">
                                        No scans found. Start a new scan to see history here.
                                    </td>
                                </tr>
                            ) : (
                                scans.map((scan) => (
                                    <tr key={scan.id} className="hover:bg-[var(--bg-main)] transition-colors">
                                        <td className="px-6 py-4 text-sm text-[var(--text-main)]">
                                            <div className="flex items-center gap-2">
                                                <Calendar className="w-4 h-4 text-[var(--color-primary)]" />
                                                {new Date(scan.timestamp).toLocaleString()}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-[var(--text-main)] font-medium">
                                            {scan.project_path.split('/').pop()}
                                            <div className="text-xs text-[var(--text-muted)] truncate max-w-[200px]">
                                                {scan.project_path}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border
                        ${scan.smell_score > 50 ? 'bg-white text-black border-black' :
                                                    scan.smell_score > 20 ? 'bg-gray-100 text-gray-800 border-gray-300' :
                                                        'bg-white text-gray-600 border-gray-200'}`}>
                                                {scan.smell_score.toFixed(1)}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-[var(--text-muted)]">
                                            {scan.files_scanned}
                                        </td>
                                        <td className="px-6 py-4 text-sm text-[var(--text-muted)]">
                                            {(scan.scan_duration || 0).toFixed(2)}s
                                        </td>
                                        <td className="px-6 py-4 text-right space-x-3">
                                            <button
                                                onClick={() => handleExport(scan.id)}
                                                className="text-[var(--color-primary)] hover:text-[var(--color-secondary)] transition-colors"
                                                title="Export PDF"
                                            >
                                                <Download className="w-5 h-5" />
                                            </button>
                                            <button
                                                onClick={() => handleLoad(scan.id)}
                                                className="text-[var(--color-primary)] hover:text-[var(--color-secondary)] transition-colors"
                                                title="View Details"
                                            >
                                                <ArrowRight className="w-5 h-5" />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default History;
