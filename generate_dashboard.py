import json
from pathlib import Path

def main():
    html_template = """<!DOCTYPE html>
<html lang="id" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard SPMB 2026 - SMPN 1 & SMPN 3 Bogor</title>
    <!-- Google Fonts Poppins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- SheetJS for Excel Export -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <style>
        :root {
            /* Dark Mode colors */
            --bg-color: #0b0f17;
            --card-bg: #151b26;
            --card-border: #242f41;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --secondary: #10b981;
            --accent: #f59e0b;
            --table-header-bg: #1e293b;
            --table-row-hover: #1f293d;
            --shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
            --gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --alert-bg: rgba(239, 68, 68, 0.1);
            --alert-border: rgba(239, 68, 68, 0.3);
            --alert-text: #ef4444;
        }

        html.light {
            /* Light Mode colors */
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --card-border: #e2e8f0;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #4f46e5;
            --primary-hover: #3730a3;
            --secondary: #059669;
            --accent: #d97706;
            --table-header-bg: #f1f5f9;
            --table-row-hover: #f8fafc;
            --shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.05);
            --gradient: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            --alert-bg: rgba(239, 68, 68, 0.05);
            --alert-border: rgba(239, 68, 68, 0.2);
            --alert-text: #b91c1c;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Header section */
        header {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--gradient);
        }

        .header-title {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .header-logo {
            width: 55px;
            height: 55px;
            background: var(--gradient);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 1.5rem;
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.4);
        }

        .header-info h1 {
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .header-info p {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 0.2rem;
        }

        .header-badges {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .badge {
            background: var(--table-header-bg);
            border: 1px solid var(--card-border);
            padding: 0.5rem 1rem;
            border-radius: 30px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
        }

        .badge-accent {
            border-color: var(--primary);
            color: var(--primary);
        }

        /* CORS fallback alert */
        .cors-alert {
            background: var(--alert-bg);
            border: 1px solid var(--alert-border);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            color: var(--text-main);
            box-shadow: var(--shadow);
        }

        .cors-alert h4 {
            color: var(--alert-text);
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .cors-alert code {
            background: rgba(0, 0, 0, 0.2);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
        }

        .drag-drop-zone {
            border: 2px dashed var(--primary);
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
            cursor: pointer;
            background: rgba(99, 102, 241, 0.05);
            transition: all 0.2s ease;
        }

        .drag-drop-zone:hover {
            background: rgba(99, 102, 241, 0.1);
        }

        /* Mode & Controls */
        .controls-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }

        .theme-toggle {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            width: 45px;
            height: 45px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: var(--shadow);
        }

        .theme-toggle:hover {
            transform: scale(1.05);
            border-color: var(--primary);
        }

        /* Tabs */
        .tabs {
            display: flex;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 0.4rem;
            border-radius: 12px;
            gap: 0.2rem;
            box-shadow: var(--shadow);
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.7rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.2s ease;
        }

        .tab-btn:hover {
            color: var(--text-main);
        }

        .tab-btn.active {
            background: var(--gradient);
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }

        /* Sub-pathway tabs */
        .sub-tabs-container {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }
        .sub-tab-btn {
            font-size: 0.85rem !important;
            padding: 0.4rem 1.2rem !important;
            border-radius: 8px !important;
        }

        /* Export buttons */
        .action-buttons {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .btn {
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
            box-shadow: var(--shadow);
        }

        .btn-primary {
            background: var(--primary);
            border: 1px solid var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }

        .btn-outline {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-main);
        }

        .btn-outline:hover {
            border-color: var(--primary);
            transform: translateY(-1px);
        }

        /* Statistics Section - 5 Serangkai */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            position: relative;
        }

        .stat-card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stat-card h3 span {
            font-size: 0.8rem;
            background: var(--table-header-bg);
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            color: var(--primary);
        }

        /* Box Plot Visualizer */
        .box-plot-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            margin-top: 0.5rem;
        }

        .box-plot-track {
            height: 12px;
            background: var(--table-header-bg);
            border-radius: 6px;
            position: relative;
            margin: 1.5rem 1rem 0.5rem 1rem;
        }

        .box-plot-iqr {
            position: absolute;
            height: 20px;
            top: -4px;
            background: rgba(99, 102, 241, 0.25);
            border: 2px solid var(--primary);
            border-radius: 4px;
        }

        .box-plot-median-line {
            position: absolute;
            width: 4px;
            height: 28px;
            top: -8px;
            background: var(--secondary);
            border-radius: 2px;
            z-index: 2;
        }

        .box-plot-whisker {
            position: absolute;
            height: 12px;
            width: 2px;
            background: var(--text-muted);
            top: 0;
        }

        .box-plot-marker {
            position: absolute;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent);
            top: 1px;
            transform: translateX(-50%);
        }

        /* 5 Serangkai Table representation */
        .serangkai-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            text-align: center;
            border: 1px solid var(--card-border);
            border-radius: 12px;
            overflow: hidden;
            background: var(--bg-color);
        }

        .serangkai-cell {
            padding: 0.75rem 0.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            border-right: 1px solid var(--card-border);
        }

        .serangkai-cell:last-child {
            border-right: none;
        }

        .serangkai-label {
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--text-muted);
        }

        .serangkai-value {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-main);
        }

        .serangkai-median {
            background: rgba(16, 185, 129, 0.08);
        }
        .serangkai-median .serangkai-value {
            color: var(--secondary);
        }

        /* Search & Table Card */
        .table-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
            flex: 1;
        }

        .table-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .search-container {
            position: relative;
            max-width: 400px;
            width: 100%;
        }

        .search-input {
            width: 100%;
            background: var(--bg-color);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            border-radius: 10px;
            font-size: 0.9rem;
            outline: none;
        }

        .search-input:focus {
            border-color: var(--primary);
        }

        .search-icon {
            position: absolute;
            left: 0.9rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        /* Table wrapper */
        .table-wrapper {
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid var(--card-border);
            max-height: 500px;
            overflow-y: auto;
            position: relative;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.88rem;
        }

        th {
            background: var(--table-header-bg);
            color: var(--text-main);
            font-weight: 600;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 10;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }

        th:hover {
            background: var(--card-border);
        }

        th.sorted-asc::after {
            content: ' ▲';
            color: var(--primary);
        }

        th.sorted-desc::after {
            content: ' ▼';
            color: var(--primary);
        }

        td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--card-border);
            color: var(--text-main);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: var(--table-row-hover);
        }

        /* Top 3 Highlighting */
        .rank-medal {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            font-size: 0.75rem;
            font-weight: 700;
            color: #fff;
            margin-right: 0.5rem;
        }

        .medal-1 {
            background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
            box-shadow: 0 2px 6px rgba(241, 196, 15, 0.4);
        }
        .medal-2 {
            background: linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%);
            box-shadow: 0 2px 6px rgba(189, 195, 199, 0.4);
        }
        .medal-3 {
            background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
            box-shadow: 0 2px 6px rgba(230, 126, 34, 0.4);
        }

        .highlight-row {
            font-weight: 500;
        }

        .highlight-row-1 {
            background: rgba(241, 196, 15, 0.03);
        }

        /* Empty state */
        .empty-state {
            padding: 3rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 1rem;
        }

        .footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        /* Box plot details */
        .plot-labels {
            display: flex;
            justify-content: space-between;
            font-size: 0.7rem;
            color: var(--text-muted);
            margin: 0.5rem 0.5rem 0 0.5rem;
        }

        .total-badge {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }
            header {
                flex-direction: column;
                align-items: flex-start;
            }
            .controls-row {
                flex-direction: column;
                align-items: stretch;
            }
            .tabs {
                flex-direction: column;
            }
        }

        /* Quota Cutoff Line Styling */
        .quota-cutoff-row td {
            padding: 0.8rem 0 !important;
            border-bottom: none !important;
            background: transparent !important;
        }

        .quota-cutoff-line {
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            margin: 0.8rem 0;
        }

        .quota-cutoff-line::before {
            content: '';
            position: absolute;
            left: 0;
            right: 0;
            height: 3px;
            background: #ef4444; /* Thicker Bright Red */
            z-index: 1;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.6);
        }

        .quota-cutoff-text {
            background: var(--card-bg);
            color: #ef4444;
            padding: 0.45rem 1.75rem;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 2px;
            border: 2px solid #ef4444;
            border-radius: 30px;
            z-index: 2;
            box-shadow: var(--shadow);
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Dimmed rows for students outside quota */
        tr.outside-quota {
            opacity: 0.38 !important;
            background: rgba(239, 68, 68, 0.02) !important;
        }

        html.light tr.outside-quota {
            background: rgba(15, 23, 42, 0.04) !important;
        }

        tr.outside-quota:hover {
            opacity: 0.95 !important;
            background-color: var(--table-row-hover) !important;
        }

        /* Border highlights for clear admission standing */
        tr:not(.outside-quota):not(.quota-cutoff-row) td:first-child {
            border-left: 4px solid var(--secondary) !important;
        }

        tr.outside-quota td:first-child {
            border-left: 4px solid var(--alert-text) !important;
        }

        /* Status pills */
        .status-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .pill-safe {
            background: rgba(16, 185, 129, 0.12);
            color: var(--secondary);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .pill-out {
            background: rgba(239, 68, 68, 0.12);
            color: var(--alert-text);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        /* Modern styled school selection dropdown selector */
        .school-dropdown {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.6rem 2.2rem 0.6rem 1rem;
            border-radius: 10px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            outline: none;
            box-shadow: var(--shadow);
            appearance: none;
            background-image: url("data:image/svg+xml;utf8,<svg fill='%236366f1' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
            background-repeat: no-repeat;
            background-position: right 8px center;
            background-size: 20px;
            transition: all 0.2s ease;
        }

        .school-dropdown:hover, .school-dropdown:focus {
            border-color: var(--primary);
            box-shadow: 0 0 8px rgba(99, 102, 241, 0.2);
        }

        /* School badges in Sekolah Tujuan column */
        .school-tag {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .tag-smpn1 {
            background: rgba(99, 102, 241, 0.15);
            color: var(--primary);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .tag-smpn3 {
            background: rgba(168, 85, 247, 0.15);
            color: #a855f7;
            border: 1px solid rgba(168, 85, 247, 0.3);
        }

        /* Sekolah Tujuan Column Toggle */
        .sekolah-col {
            display: none;
        }
        body.show-sekolah .sekolah-col {
            display: table-cell;
        }
    </style>
</head>
<body>

    <header>
        <div class="header-title">
            <div class="header-logo">SPMB</div>
            <div class="header-info">
                <h1 id="school-name">Memuat Data Sekolah...</h1>
                <p id="school-update">Sistem Penerimaan Murid Baru (SPMB) 2026</p>
            </div>
        </div>
        <div class="header-badges">
            <div class="badge badge-accent">
                <span>NPSN:</span> <strong id="school-npsn">-</strong>
            </div>
            <div class="badge">
                <span>Total Pendaftar Terverifikasi:</span> <strong id="school-total">-</strong>
            </div>
            <div class="badge">
                <span>Update Data:</span> <span id="last-update">-</span>
            </div>
        </div>
    </header>

    <!-- CORS Warning and File uploader (Shown if loading fails) -->
    <div class="cors-alert" id="cors-alert" style="display: none;">
        <h4>⚠️ Gagal Memuat Data Secara Otomatis (CORS Policy)</h4>
        <p>Browser memblokir permintaan berkas lokal <code>pendaftar_data.json</code> demi alasan keamanan saat dibuka langsung menggunakan <code>file://</code> (klik dua kali).</p>
        <p><strong>Solusi:</strong></p>
        <ol style="margin-left: 1.5rem; display: flex; flex-direction: column; gap: 0.4rem;">
            <li>Jalankan server lokal melalui terminal: <code>python3 -m http.server 8000</code> lalu buka <code>http://localhost:8000</code>.</li>
            <li>Unggah file <code>pendaftar_data.json</code> secara manual menggunakan kotak di bawah ini:</li>
        </ol>
        <div class="drag-drop-zone" id="drop-zone">
            Drag & Drop berkas <strong>pendaftar_data.json</strong> ke sini, atau klik untuk memilih berkas
            <input type="file" id="file-input" style="display: none;" accept=".json">
        </div>
    </div>

    <!-- Main Navigation controls (School switcher) -->
    <div class="controls-row">
        <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
            <button class="theme-toggle" id="theme-toggle" title="Toggle Light/Dark Mode">🌙</button>
            
            <!-- School Selection Dropdown Selector -->
            <div style="position: relative;">
                <select id="school-select" class="school-dropdown" onchange="switchSchool(this.value)">
                    <option value="semua">Semua Sekolah (SMPN 1 & SMPN 3)</option>
                    <option value="smpn1">SMPN 1 Bogor</option>
                    <option value="smpn3">SMPN 3 Bogor</option>
                </select>
            </div>
            
            <!-- Pathway Tabs -->
            <div class="tabs" id="pathway-tabs">
                <button class="tab-btn active" onclick="switchPathway('prestasi')">Prestasi</button>
                <button class="tab-btn" onclick="switchPathway('domisili')">Domisili</button>
                <button class="tab-btn" onclick="switchPathway('afirmasi')">Afirmasi</button>
                <button class="tab-btn" onclick="switchPathway('mutasi')">Mutasi</button>
            </div>

            <!-- Dalam/Luar Kota Tabs -->
            <div class="tabs" id="residency-tabs">
                <button class="tab-btn active" onclick="switchResidency('semua')">Semua Domisili</button>
                <button class="tab-btn" onclick="switchResidency('dalam')">Dalam Kota</button>
                <button class="tab-btn" onclick="switchResidency('luar')">Luar Kota</button>
            </div>
        </div>

        <div class="action-buttons">
            <button class="btn btn-outline" onclick="exportCurrentToExcel()">📊 Export View Saat Ini</button>
            <button class="btn btn-primary" onclick="exportSchoolToExcel()">📥 Export Sekolah Aktif</button>
        </div>
    </div>

    <!-- Sub-pathways Menu specifically for Prestasi -->
    <div class="sub-tabs-container" id="sub-tabs-container" style="display: flex; margin-bottom: 1rem; margin-top: -1rem;">
        <div class="tabs" style="font-size: 0.9rem; padding: 0.3rem;">
            <button class="tab-btn sub-tab-btn active" onclick="switchSubPathway('semua')">Semua Prestasi</button>
            <button class="tab-btn sub-tab-btn" onclick="switchSubPathway('rapor')">Prestasi Rapor (Total RAPOR + TKA)</button>
            <button class="tab-btn sub-tab-btn" onclick="switchSubPathway('akademik')">Prestasi Akademik / Non Akademik</button>
        </div>
    </div>

    <!-- Statistics Section - Statistik 5 Serangkai -->
    <div class="stats-grid" id="stats-container">
        <!-- Will be populated dynamically -->
    </div>

    <!-- Table Card -->
    <div class="table-card">
        <div class="table-header-row">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <h2 style="font-size: 1.2rem; font-weight: 600;" id="table-title">Daftar Pendaftar - Jalur Prestasi</h2>
                <div class="total-badge" id="filtered-count">Memuat pendaftar...</div>
            </div>
            <div class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" id="search-bar" placeholder="Cari berdasarkan nama murid atau asal sekolah..." oninput="handleSearch()">
            </div>
        </div>
        
        <!-- Disclaimer note under table headers -->
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: -0.5rem; display: flex; align-items: center; gap: 0.4rem; padding: 0 0.5rem;">
            <span>ℹ️</span> <em>Hasil ini bukan passing grade resmi, tapi hanya berdasarkan kuota dari masing masing jalur di website disdik kota bogor</em>
        </div>

        <div class="table-wrapper">
            <table id="pendaftar-table">
                <thead>
                    <tr>
                        <th onclick="handleSort('rank')">No</th>
                        <th onclick="handleSort('no_pendaftaran')">No. Pendaftaran</th>
                        <th onclick="handleSort('nama_murid')">Nama Murid</th>
                        <th onclick="handleSort('asal_satuan_pendidikan')">Asal Sekolah</th>
                        <th class="sekolah-col" onclick="handleSort('schoolKey')">Sekolah Tujuan</th>
                        <th onclick="handleSort('sub_jalur')">Sub Jalur</th>
                        <th onclick="handleSort('nilai_rapor')">Total RAPOR + TKA</th>
                        <th onclick="handleSort('jarak')">Jarak (m)</th>
                        <th onclick="handleSort('skor_sertifikat')">Skor Sertifikat</th>
                        <th onclick="handleSort('status_domisili')">Domisili</th>
                        <th onclick="handleSort('skor_akhir')">Skor Akhir</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    <!-- Will be populated dynamically -->
                </tbody>
            </table>
            <div id="table-empty" class="empty-state" style="display: none;">
                Tidak ada data pendaftar yang cocok dengan filter atau pencarian Anda.
            </div>
        </div>
    </div>

    <div class="footer">
        Portal SPMB Bogor 2026 &copy; Dashboard & Statistik Terintegrasi (Real-time update via GitHub Action).
    </div>

    <script>
        let spmbData = null; // Loaded dynamically
        let currentSchool = 'smpn1';
        let currentPathway = 'prestasi';
        let currentSubPathway = 'semua';
        let currentResidency = 'semua'; // semua, dalam, luar
        let filteredApplicants = [];
        let sortConfig = { key: 'nilai_rapor', direction: 'desc' };

        // Init page
        document.addEventListener('DOMContentLoaded', () => {
            loadData();
            
            // Theme toggle
            const themeBtn = document.getElementById('theme-toggle');
            themeBtn.addEventListener('click', () => {
                const htmlEl = document.documentElement;
                if (htmlEl.classList.contains('dark')) {
                    htmlEl.classList.remove('dark');
                    htmlEl.classList.add('light');
                    themeBtn.textContent = '☀️';
                } else {
                    htmlEl.classList.remove('light');
                    htmlEl.classList.add('dark');
                    themeBtn.textContent = '🌙';
                }
            });

            // Set up manual uploader trigger
            const dropZone = document.getElementById('drop-zone');
            const fileInput = document.getElementById('file-input');
            
            dropZone.addEventListener('click', () => fileInput.click());
            
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleUploadedFile(e.target.files[0]);
                }
            });

            // Drag and drop events
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.style.background = 'rgba(99, 102, 241, 0.15)';
            });

            dropZone.addEventListener('dragleave', () => {
                dropZone.style.background = 'rgba(99, 102, 241, 0.05)';
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.style.background = 'rgba(99, 102, 241, 0.05)';
                if (e.dataTransfer.files.length > 0) {
                    handleUploadedFile(e.dataTransfer.files[0]);
                }
            });
        });

        // Compute official rank and safe status for all pathways
        function computeOfficialStatus() {
            if (!spmbData) return;
            
            // Loop through each school
            for (const schoolKey of ['smpn1', 'smpn3']) {
                const schoolData = spmbData.schools[schoolKey] || {};
                const pathways = schoolData.pathways || {};
                
                // 1. Domisili (quota = 130)
                if (pathways.domisili) {
                    const domisiliList = [...pathways.domisili];
                    domisiliList.sort((a, b) => {
                        const wilA = a.sub_jalur || a.subJalur || '';
                        const wilB = b.sub_jalur || b.subJalur || '';
                        if (wilA !== wilB) return wilA.localeCompare(wilB);
                        const jarA = parseFloat(a.jarak) || Infinity;
                        const jarB = parseFloat(b.jarak) || Infinity;
                        if (jarA !== jarB) return jarA - jarB;
                        return (a.no_pendaftaran || '').localeCompare(b.no_pendaftaran || '');
                    });
                    domisiliList.forEach((app, idx) => {
                        const originalApp = pathways.domisili.find(x => x.no_pendaftaran === app.no_pendaftaran);
                        if (originalApp) {
                            originalApp.officialRank = idx + 1;
                            originalApp.isSafe = (idx + 1) <= 130;
                        }
                    });
                }

                // 2. Afirmasi (quota = 81)
                if (pathways.afirmasi) {
                    const afirmasiList = [...pathways.afirmasi];
                    afirmasiList.sort((a, b) => {
                        const jarA = parseFloat(a.jarak) || Infinity;
                        const jarB = parseFloat(b.jarak) || Infinity;
                        if (jarA !== jarB) return jarA - jarB;
                        return (a.no_pendaftaran || '').localeCompare(b.no_pendaftaran || '');
                    });
                    afirmasiList.forEach((app, idx) => {
                        const originalApp = pathways.afirmasi.find(x => x.no_pendaftaran === app.no_pendaftaran);
                        if (originalApp) {
                            originalApp.officialRank = idx + 1;
                            originalApp.isSafe = (idx + 1) <= 81;
                        }
                    });
                }

                // 3. Mutasi (quota = 16)
                if (pathways.mutasi) {
                    const mutasiList = [...pathways.mutasi];
                    mutasiList.sort((a, b) => {
                        const jarA = parseFloat(a.jarak) || Infinity;
                        const jarB = parseFloat(b.jarak) || Infinity;
                        if (jarA !== jarB) return jarA - jarB;
                        return (a.no_pendaftaran || '').localeCompare(b.no_pendaftaran || '');
                    });
                    mutasiList.forEach((app, idx) => {
                        const originalApp = pathways.mutasi.find(x => x.no_pendaftaran === app.no_pendaftaran);
                        if (originalApp) {
                            originalApp.officialRank = idx + 1;
                            originalApp.isSafe = (idx + 1) <= 16;
                        }
                    });
                }

                // 4. Prestasi
                if (pathways.prestasi) {
                    // Prestasi Rapor (quota = 48)
                    const raporApps = pathways.prestasi.filter(app => app.sub_jalur === 'Prestasi Rapor');
                    raporApps.sort((a, b) => {
                        const valA = parseFloat(a.nilai_rapor) || -Infinity;
                        const valB = parseFloat(b.nilai_rapor) || -Infinity;
                        if (valA !== valB) return valB - valA;
                        return (a.no_pendaftaran || '').localeCompare(b.no_pendaftaran || '');
                    });
                    raporApps.forEach((app, idx) => {
                        app.officialRank = idx + 1;
                        app.isSafe = (idx + 1) <= 48;
                    });

                    // Prestasi Akademik (quota = 49)
                    const akademikApps = pathways.prestasi.filter(app => app.sub_jalur === 'Prestasi Akademik/Non Akademik');
                    akademikApps.sort((a, b) => {
                        const valA = parseFloat(a.skor_sertifikat) || -Infinity;
                        const valB = parseFloat(b.skor_sertifikat) || -Infinity;
                        if (valA !== valB) return valB - valA;
                        return (a.no_pendaftaran || '').localeCompare(b.no_pendaftaran || '');
                    });
                    akademikApps.forEach((app, idx) => {
                        app.officialRank = idx + 1;
                        app.isSafe = (idx + 1) <= 49;
                    });
                }
            }
        }

        // Load data dynamically
        function loadData() {
            fetch('./pendaftar_data.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    spmbData = data;
                    computeOfficialStatus();
                    document.getElementById('cors-alert').style.display = 'none';
                    initDashboard();
                })
                .catch(err => {
                    console.warn('CORS or file access issue, showing manual uploader fallback:', err);
                    document.getElementById('cors-alert').style.display = 'flex';
                    document.getElementById('filtered-count').textContent = 'Silakan unggah berkas data...';
                });
        }

        // Handle manually uploaded pendaftar_data.json
        function handleUploadedFile(file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (data.schools) {
                        spmbData = data;
                        computeOfficialStatus();
                        document.getElementById('cors-alert').style.display = 'none';
                        initDashboard();
                        alert('Data pendaftar_data.json berhasil dimuat secara lokal!');
                    } else {
                        alert('Format berkas salah. Berkas harus berupa pendaftar_data.json yang sah.');
                    }
                } catch (err) {
                    alert('Gagal membaca berkas JSON: ' + err.message);
                }
            };
            reader.readAsText(file);
        }

        function initDashboard() {
            document.getElementById('school-select').value = 'semua';
            switchSchool('semua');
        }

        function initSchoolInfo() {
            if (!spmbData || !spmbData.schools) return;

            if (currentSchool === 'semua') {
                document.getElementById('school-name').textContent = 'Semua Sekolah (SMPN 1 & SMPN 3)';
                document.getElementById('school-npsn').textContent = 'Multi-NPSN';
                
                // Sum verified applicants
                let totalVerified = 0;
                totalVerified += spmbData.schools['smpn1']?.info?.jumlah_terverifikasi || 0;
                totalVerified += spmbData.schools['smpn3']?.info?.jumlah_terverifikasi || 0;
                document.getElementById('school-total').textContent = totalVerified;
                
                // Get latest update time
                const up1 = spmbData.schools['smpn1']?.info?.terakhir_diperbarui || '';
                const up3 = spmbData.schools['smpn3']?.info?.terakhir_diperbarui || '';
                const lastUpdate = up1 > up3 ? up1 : (up3 || up1 || '-');
                document.getElementById('last-update').textContent = lastUpdate;
            } else {
                const school = spmbData.schools[currentSchool] || {};
                const info = school.info || {};
                document.getElementById('school-name').textContent = info.nama_satuan_pendidikan || 'Memuat Sekolah...';
                document.getElementById('school-npsn').textContent = info.npsn || '-';
                document.getElementById('school-total').textContent = info.jumlah_terverifikasi || '-';
                document.getElementById('last-update').textContent = info.terakhir_diperbarui || '-';
            }
        }

        function switchSchool(schoolKey) {
            currentSchool = schoolKey;
            
            // Synchronize dropdown value
            document.getElementById('school-select').value = schoolKey;

            // Toggle show-sekolah class on body to control column visibility
            if (schoolKey === 'semua') {
                document.body.classList.add('show-sekolah');
            } else {
                document.body.classList.remove('show-sekolah');
            }

            initSchoolInfo();
            switchPathway(currentPathway); // Refresh view
        }

        function switchPathway(pathwayKey) {
            currentPathway = pathwayKey;
            
            // Update active pathway tab style
            const tabButtons = document.querySelectorAll('#pathway-tabs .tab-btn');
            tabButtons.forEach(btn => {
                if (btn.textContent.toLowerCase().includes(pathwayKey)) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Show/hide sub-pathway tabs
            const subTabs = document.getElementById('sub-tabs-container');
            if (pathwayKey === 'prestasi') {
                subTabs.style.display = 'flex';
                currentSubPathway = 'semua';
                
                // Reset sub-tabs active state
                const subBtns = document.querySelectorAll('.sub-tab-btn');
                subBtns.forEach((btn, idx) => {
                    if (idx === 0) btn.classList.add('active');
                    else btn.classList.remove('active');
                });
            } else {
                subTabs.style.display = 'none';
            }

            // Set default sort config based on pathway
            if (pathwayKey === 'prestasi') {
                sortConfig = { key: 'nilai_rapor', direction: 'desc' }; // Rapor desc for combined view
            } else {
                sortConfig = { key: 'rank', direction: 'asc' }; // official rank asc
            }

            // Reset search bar
            document.getElementById('search-bar').value = '';

            // Update title
            const nameMap = {
                'prestasi': 'Jalur Prestasi',
                'domisili': 'Jalur Domisili',
                'afirmasi': 'Jalur Afirmasi',
                'mutasi': 'Jalur Mutasi'
            };
            const schoolNameShort = currentSchool === 'semua' ? 'Semua Sekolah' : currentSchool.toUpperCase();
            document.getElementById('table-title').textContent = `Daftar Pendaftar - ${nameMap[pathwayKey]} (${schoolNameShort})`;

            applyFiltersAndSort();
            renderStats();
        }

        function switchSubPathway(subPathwayKey) {
            currentSubPathway = subPathwayKey;

            // Update sub-tab active style
            const subTabButtons = document.querySelectorAll('.sub-tab-btn');
            subTabButtons.forEach(btn => {
                const text = btn.textContent.toLowerCase();
                if (
                    (subPathwayKey === 'semua' && text.includes('semua')) ||
                    (subPathwayKey === 'rapor' && text.includes('rapor')) ||
                    (subPathwayKey === 'akademik' && text.includes('akademik'))
                ) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Set sort key depending on subpathway
            if (subPathwayKey === 'semua') {
                sortConfig = { key: 'nilai_rapor', direction: 'desc' };
            } else {
                sortConfig = { key: 'rank', direction: 'asc' };
            }

            applyFiltersAndSort();
            renderStats();
        }

        function switchResidency(residencyKey) {
            currentResidency = residencyKey;
            
            // Update residency buttons active class
            const resBtns = document.querySelectorAll('#residency-tabs .tab-btn');
            resBtns.forEach(btn => {
                const text = btn.textContent.toLowerCase();
                if (
                    (residencyKey === 'semua' && text.includes('semua')) ||
                    (residencyKey === 'dalam' && text.includes('dalam')) ||
                    (residencyKey === 'luar' && text.includes('luar'))
                ) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            applyFiltersAndSort();
            renderStats();
        }

        function applyFiltersAndSort() {
            if (!spmbData) return;
            
            const searchQuery = document.getElementById('search-bar').value.toLowerCase().trim();
            
            let applicants = [];
            if (currentSchool === 'semua') {
                const smpn1List = spmbData.schools['smpn1']?.pathways[currentPathway] || [];
                const smpn3List = spmbData.schools['smpn3']?.pathways[currentPathway] || [];
                applicants = [
                    ...smpn1List.map(app => ({ ...app, schoolKey: 'smpn1' })),
                    ...smpn3List.map(app => ({ ...app, schoolKey: 'smpn3' }))
                ];
            } else {
                const schoolData = spmbData.schools[currentSchool] || {};
                const list = schoolData.pathways[currentPathway] || [];
                applicants = list.map(app => ({ ...app, schoolKey: currentSchool }));
            }

            // 1. Filter by sub-pathway (Prestasi only)
            if (currentPathway === 'prestasi') {
                if (currentSubPathway === 'rapor') {
                    applicants = applicants.filter(app => app.sub_jalur === 'Prestasi Rapor');
                } else if (currentSubPathway === 'akademik') {
                    applicants = applicants.filter(app => app.sub_jalur === 'Prestasi Akademik/Non Akademik');
                }
            }

            // 2. Filter by Residency (Dalam Kota / Luar Kota)
            if (currentResidency === 'dalam') {
                applicants = applicants.filter(app => (app.status_domisili || '').toLowerCase().includes('dalam'));
            } else if (currentResidency === 'luar') {
                applicants = applicants.filter(app => (app.status_domisili || '').toLowerCase().includes('luar'));
            }

            // 3. Search Filter
            filteredApplicants = applicants.filter(app => {
                const name = (app.nama_murid || '').toLowerCase();
                const school = (app.asal_satuan_pendidikan || '').toLowerCase();
                const regNo = (app.no_pendaftaran || '').toLowerCase();
                return name.includes(searchQuery) || school.includes(searchQuery) || regNo.includes(searchQuery);
            });

            // Helper to parse values for sorting
            const getSortVal = (app, key) => {
                if (key === 'rank') {
                    return app.officialRank || 9999;
                }
                if (key === 'schoolKey') {
                    return app.schoolKey || '';
                }
                let val = app[key];
                
                // Hide report score for academic pendaftar because it's duplicate of cert score
                if (key === 'nilai_rapor' && app.sub_jalur === 'Prestasi Akademik/Non Akademik') {
                    val = '-';
                }
                // Hide certificate score for report pendaftar
                if (key === 'skor_sertifikat' && app.sub_jalur === 'Prestasi Rapor') {
                    val = '-';
                }

                if (val === undefined || val === null || val === '-') {
                    return sortConfig.direction === 'asc' ? Infinity : -Infinity;
                }
                if (key === 'nilai_rapor' || key === 'skor_sertifikat' || key === 'jarak' || key === 'skor_akhir') {
                    const parsed = parseFloat(val);
                    return isNaN(parsed) ? (sortConfig.direction === 'asc' ? Infinity : -Infinity) : parsed;
                }
                return val;
            };

            // 4. Sort
            filteredApplicants.sort((a, b) => {
                // Special official sorting for Domisili when sorting by rank or default
                if (currentPathway === 'domisili' && (sortConfig.key === 'rank' || (sortConfig.key === 'jarak' && sortConfig.direction === 'asc'))) {
                    const wilA = a.sub_jalur || a.subJalur || '';
                    const wilB = b.sub_jalur || b.subJalur || '';
                    if (wilA !== wilB) {
                        return sortConfig.direction === 'asc' ? wilA.localeCompare(wilB) : wilB.localeCompare(wilA);
                    }
                }
                
                const valA = getSortVal(a, sortConfig.key);
                const valB = getSortVal(b, sortConfig.key);

                if (valA < valB) return sortConfig.direction === 'asc' ? -1 : 1;
                if (valA > valB) return sortConfig.direction === 'asc' ? 1 : -1;
                return 0;
            });

            // Update filtered count label
            document.getElementById('filtered-count').textContent = `Menampilkan ${filteredApplicants.length} dari ${applicants.length} pendaftar`;

            renderTable();
        }

        function handleSearch() {
            applyFiltersAndSort();
        }

        function handleSort(key) {
            if (sortConfig.key === key) {
                // toggle direction
                sortConfig.direction = sortConfig.direction === 'asc' ? 'desc' : 'asc';
            } else {
                sortConfig.key = key;
                sortConfig.direction = (key === 'nilai_rapor' || key === 'skor_sertifikat' || key === 'skor_akhir') ? 'desc' : 'asc';
            }

            // Update header class
            const headers = document.querySelectorAll('th');
            headers.forEach(th => {
                th.classList.remove('sorted-asc', 'sorted-desc');
                const onclickAttr = th.getAttribute('onclick');
                if (onclickAttr && onclickAttr.includes(`'${key}'`)) {
                    th.classList.add(sortConfig.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
                }
            });

            applyFiltersAndSort();
        }

        function getQuotaLimit() {
            if (currentPathway === 'domisili') return 130;
            if (currentPathway === 'afirmasi') return 81;
            if (currentPathway === 'mutasi') return 16;
            if (currentPathway === 'prestasi') {
                if (currentSubPathway === 'rapor') return 48;
                if (currentSubPathway === 'akademik') return 49;
                if (currentSubPathway === 'semua') return 97;
            }
            return 0;
        }

        function renderTable() {
            const tbody = document.getElementById('table-body');
            const emptyState = document.getElementById('table-empty');
            tbody.innerHTML = '';

            if (filteredApplicants.length === 0) {
                emptyState.style.display = 'block';
                return;
            } else {
                emptyState.style.display = 'none';
            }

            const quotaLimit = getQuotaLimit();
            const isOfficialOrder = (
                currentSchool !== 'semua' && // Disable cutoff line for combined view
                document.getElementById('search-bar').value.toLowerCase().trim() === '' &&
                currentResidency === 'semua' &&
                (
                    sortConfig.key === 'rank' ||
                    (currentPathway === 'domisili' && sortConfig.key === 'jarak' && sortConfig.direction === 'asc') ||
                    (currentPathway === 'afirmasi' && sortConfig.key === 'jarak' && sortConfig.direction === 'asc') ||
                    (currentPathway === 'mutasi' && sortConfig.key === 'jarak' && sortConfig.direction === 'asc') ||
                    (currentPathway === 'prestasi' && currentSubPathway === 'semua' && sortConfig.key === 'nilai_rapor' && sortConfig.direction === 'desc') ||
                    (currentPathway === 'prestasi' && currentSubPathway === 'rapor' && sortConfig.key === 'nilai_rapor' && sortConfig.direction === 'desc') ||
                    (currentPathway === 'prestasi' && currentSubPathway === 'akademik' && sortConfig.key === 'skor_sertifikat' && sortConfig.direction === 'desc')
                )
            );

            filteredApplicants.forEach((app, idx) => {
                const tr = document.createElement('tr');
                const rankNum = idx + 1;

                // Add classes for styling rank 1, 2, 3
                if (rankNum <= 3) {
                    tr.classList.add('highlight-row', `highlight-row-${rankNum}`);
                }

                // Add class if outside quota
                const isSafe = app.isSafe !== false;
                if (!isSafe) {
                    tr.classList.add('outside-quota');
                }

                let rankCell = rankNum.toString();
                if (rankNum === 1) rankCell = `<span class="rank-medal medal-1">1</span>`;
                else if (rankNum === 2) rankCell = `<span class="rank-medal medal-2">2</span>`;
                else if (rankNum === 3) rankCell = `<span class="rank-medal medal-3">3</span>`;

                // Calculate which scores to display based on sub_jalur
                let totalRaporTka = '-';
                let skorSertifikat = '-';

                if (app.sub_jalur === 'Prestasi Rapor') {
                    totalRaporTka = app.nilai_rapor || '-';
                    skorSertifikat = '-';
                } else if (app.sub_jalur === 'Prestasi Akademik/Non Akademik') {
                    totalRaporTka = '-';
                    skorSertifikat = app.skor_sertifikat || '-';
                } else {
                    totalRaporTka = app.nilai_rapor || '-';
                    skorSertifikat = app.skor_sertifikat || '-';
                }

                const statusBadge = isSafe 
                    ? `<span class="status-pill pill-safe">Aman</span>` 
                    : `<span class="status-pill pill-out">Gugur</span>`;

                const schoolTag = app.schoolKey === 'smpn1' 
                    ? '<span class="school-tag tag-smpn1">SMPN 1</span>' 
                    : '<span class="school-tag tag-smpn3">SMPN 3</span>';

                tr.innerHTML = `
                    <td>${rankCell}</td>
                    <td>${app.no_pendaftaran || '-'}</td>
                    <td>${app.nama_murid || '-'}</td>
                    <td>${app.asal_satuan_pendidikan || '-'}</td>
                    <td class="sekolah-col">${schoolTag}</td>
                    <td>${app.sub_jalur || '-'}</td>
                    <td>${totalRaporTka}</td>
                    <td>${app.jarak || '-'}</td>
                    <td>${skorSertifikat}</td>
                    <td>${app.status_domisili || '-'}</td>
                    <td>${app.skor_akhir || '-'}</td>
                    <td>${statusBadge}</td>
                `;
                tbody.appendChild(tr);

                // Insert cutoff line if in official order and exactly at the cutoff point
                if (isOfficialOrder && (idx + 1) === quotaLimit) {
                    const cutoffTr = document.createElement('tr');
                    cutoffTr.className = 'quota-cutoff-row';
                    
                    let quotaLabel = `Batas Kuota Terpenuhi (${quotaLimit} Siswa)`;
                    if (currentPathway === 'domisili') quotaLabel = `Batas Kuota Domisili Terpenuhi (130 Siswa)`;
                    if (currentPathway === 'afirmasi') quotaLabel = `Batas Kuota Afirmasi Terpenuhi (81 Siswa)`;
                    if (currentPathway === 'mutasi') quotaLabel = `Batas Kuota Mutasi Terpenuhi (16 Siswa)`;
                    if (currentPathway === 'prestasi') {
                        if (currentSubPathway === 'rapor') quotaLabel = `Batas Kuota Prestasi Rapor Terpenuhi (48 Siswa)`;
                        if (currentSubPathway === 'akademik') quotaLabel = `Batas Kuota Prestasi Akademik Terpenuhi (49 Siswa)`;
                        if (currentSubPathway === 'semua') quotaLabel = `Batas Total Kuota Prestasi Terpenuhi (97 Siswa)`;
                    }

                    cutoffTr.innerHTML = `
                        <td colspan="11">
                            <div class="quota-cutoff-line">
                                <span class="quota-cutoff-text">🛑 ${quotaLabel} 🛑</span>
                            </div>
                        </td>
                    `;
                    tbody.appendChild(cutoffTr);
                }
            });
        }

        /* Statistical calculations - 5 Serangkai */
        function getMedian(arr) {
            if (arr.length === 0) return 0;
            const mid = Math.floor(arr.length / 2);
            if (arr.length % 2 !== 0) {
                return arr[mid];
            }
            return (arr[mid - 1] + arr[mid]) / 2;
        }

        function calculateFiveNumberSummary(arr) {
            if (arr.length === 0) return { min: 0, q1: 0, median: 0, q3: 0, max: 0 };
            
            // Sort ascending
            const sorted = [...arr].sort((a, b) => a - b);
            const min = sorted[0];
            const max = sorted[sorted.length - 1];
            const median = getMedian(sorted);
            
            const mid = Math.floor(sorted.length / 2);
            let lowerHalf, upperHalf;
            
            if (sorted.length % 2 !== 0) {
                lowerHalf = sorted.slice(0, mid);
                upperHalf = sorted.slice(mid + 1);
            } else {
                lowerHalf = sorted.slice(0, mid);
                upperHalf = sorted.slice(mid);
            }
            
            const q1 = getMedian(lowerHalf);
            const q3 = getMedian(upperHalf);
            
            return { min, q1, median, q3, max };
        }

        function renderStats() {
            const container = document.getElementById('stats-container');
            container.innerHTML = '';

            if (!spmbData) return;

            let applicants = [];
            if (currentSchool === 'semua') {
                const smpn1List = spmbData.schools['smpn1']?.pathways[currentPathway] || [];
                const smpn3List = spmbData.schools['smpn3']?.pathways[currentPathway] || [];
                applicants = [
                    ...smpn1List.map(app => ({ ...app, schoolKey: 'smpn1' })),
                    ...smpn3List.map(app => ({ ...app, schoolKey: 'smpn3' }))
                ];
            } else {
                const schoolData = spmbData.schools[currentSchool] || {};
                applicants = schoolData.pathways[currentPathway] || [];
            }

            // 1. Filter applicants for statistics based on active filters
            if (currentPathway === 'prestasi') {
                if (currentSubPathway === 'rapor') {
                    applicants = applicants.filter(app => app.sub_jalur === 'Prestasi Rapor');
                } else if (currentSubPathway === 'akademik') {
                    applicants = applicants.filter(app => app.sub_jalur === 'Prestasi Akademik/Non Akademik');
                }
            }

            if (currentResidency === 'dalam') {
                applicants = applicants.filter(app => (app.status_domisili || '').toLowerCase().includes('dalam'));
            } else if (currentResidency === 'luar') {
                applicants = applicants.filter(app => (app.status_domisili || '').toLowerCase().includes('luar'));
            }

            if (applicants.length === 0) return;

            // Define which metrics we want to visualize for this pathway
            let metrics = [];
            if (currentPathway === 'prestasi') {
                if (currentSubPathway === 'semua') {
                    metrics = [
                        { 
                            name: 'Total RAPOR + TKA (Prestasi Rapor)', 
                            key: 'nilai_rapor', 
                            unit: '',
                            filterFn: app => app.sub_jalur === 'Prestasi Rapor'
                        },
                        { 
                            name: 'Skor Sertifikat (Akademik/Non Akad.)', 
                            key: 'skor_sertifikat', 
                            unit: '',
                            filterFn: app => app.sub_jalur === 'Prestasi Akademik/Non Akademik'
                        }
                    ];
                } else if (currentSubPathway === 'rapor') {
                    metrics = [
                        { 
                            name: 'Total RAPOR + TKA', 
                            key: 'nilai_rapor', 
                            unit: '',
                            filterFn: () => true
                        }
                    ];
                } else if (currentSubPathway === 'akademik') {
                    metrics = [
                        { 
                            name: 'Skor Sertifikat', 
                            key: 'skor_sertifikat', 
                            unit: '',
                            filterFn: () => true
                        }
                    ];
                }
            } else {
                metrics = [
                    { name: 'Jarak Pendaftaran', key: 'jarak', unit: ' m', filterFn: () => true }
                ];
            }

            metrics.forEach(metric => {
                // Extract numbers
                const filteredApps = applicants.filter(metric.filterFn);
                const values = filteredApps
                    .map(app => parseFloat(app[metric.key]))
                    .filter(val => !isNaN(val) && val !== null);

                if (values.length === 0) return;

                const summary = calculateFiveNumberSummary(values);
                
                // Formats for display
                const minVal = summary.min.toFixed(2);
                const q1Val = summary.q1.toFixed(2);
                const medVal = summary.median.toFixed(2);
                const q3Val = summary.q3.toFixed(2);
                const maxVal = summary.max.toFixed(2);
                const unit = metric.unit;

                // Box plot percentages
                const range = summary.max - summary.min;
                const getPct = (val) => {
                    if (range === 0) return 50;
                    return ((val - summary.min) / range) * 100;
                };

                const q1Pct = getPct(summary.q1).toFixed(1);
                const q3Pct = getPct(summary.q3).toFixed(1);
                const medPct = getPct(summary.median).toFixed(1);
                const iqrWidth = (q3Pct - q1Pct).toFixed(1);

                const card = document.createElement('div');
                card.className = 'stat-card';
                card.innerHTML = `
                    <h3>${metric.name} <span>Statistik 5 Serangkai</span></h3>
                    
                    <div class="box-plot-container">
                        <div class="box-plot-track">
                            <!-- Whiskers -->
                            <div class="box-plot-whisker" style="left: 0%; height: 20px; top: -4px;"></div>
                            <div class="box-plot-whisker" style="left: 100%; height: 20px; top: -4px;"></div>
                            <div class="box-plot-whisker" style="left: 0%; width: 100%; height: 2px; top: 5px; background: var(--text-muted);"></div>
                            
                            <!-- IQR Box -->
                            <div class="box-plot-iqr" style="left: ${q1Pct}%; width: ${iqrWidth}%;"></div>
                            
                            <!-- Median line -->
                            <div class="box-plot-median-line" style="left: ${medPct}%;"></div>
                            
                            <!-- Min and Max markers -->
                            <div class="box-plot-marker" style="left: 0%;" title="Minimum: ${minVal}${unit}"></div>
                            <div class="box-plot-marker" style="left: 100%;" title="Maksimum: ${maxVal}${unit}"></div>
                        </div>
                        <div class="plot-labels">
                            <span>Min: ${minVal}</span>
                            <span>Q1: ${q1Val}</span>
                            <span>Med: ${medVal}</span>
                            <span>Q3: ${q3Val}</span>
                            <span>Max: ${maxVal}</span>
                        </div>
                    </div>

                    <div class="serangkai-grid">
                        <div class="serangkai-cell">
                            <span class="serangkai-label">Minimum</span>
                            <span class="serangkai-value">${minVal}${unit}</span>
                        </div>
                        <div class="serangkai-cell">
                            <span class="serangkai-label">Q1 (Bawah)</span>
                            <span class="serangkai-value">${q1Val}${unit}</span>
                        </div>
                        <div class="serangkai-cell serangkai-median">
                            <span class="serangkai-label">Q2 (Median)</span>
                            <span class="serangkai-value">${medVal}${unit}</span>
                        </div>
                        <div class="serangkai-cell">
                            <span class="serangkai-label">Q3 (Atas)</span>
                            <span class="serangkai-value">${q3Val}${unit}</span>
                        </div>
                        <div class="serangkai-cell">
                            <span class="serangkai-label">Maksimum</span>
                            <span class="serangkai-value">${maxVal}${unit}</span>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        /* Excel Export functionality using SheetJS */
        function getFormattedExcelList(applicantsList) {
            return applicantsList.map((app, idx) => {
                let totalRaporTka = '-';
                let skorSertifikat = '-';

                if (app.sub_jalur === 'Prestasi Rapor') {
                    totalRaporTka = app.nilai_rapor !== '-' ? parseFloat(app.nilai_rapor) : '-';
                    skorSertifikat = '-';
                } else if (app.sub_jalur === 'Prestasi Akademik/Non Akademik') {
                    totalRaporTka = '-';
                    skorSertifikat = app.skor_sertifikat !== '-' ? parseFloat(app.skor_sertifikat) : '-';
                } else {
                    totalRaporTka = app.nilai_rapor !== '-' ? parseFloat(app.nilai_rapor) : '-';
                    skorSertifikat = app.skor_sertifikat !== '-' ? parseFloat(app.skor_sertifikat) : '-';
                }

                const item = {
                    'No': idx + 1,
                    'No. Pendaftaran': app.no_pendaftaran || '',
                    'Nama Murid': app.nama_murid || '',
                    'Asal Sekolah': app.asal_satuan_pendidikan || '',
                    'Sub Jalur': app.sub_jalur || '',
                    'Total RAPOR + TKA': totalRaporTka,
                    'Jarak (m)': app.jarak !== '-' ? parseFloat(app.jarak) : '-',
                    'Skor Sertifikat': skorSertifikat,
                    'Domisili': app.status_domisili || '',
                    'Skor Akhir': app.skor_akhir !== '-' ? parseFloat(app.skor_akhir) : '-'
                };

                if (currentSchool === 'semua' || app.schoolKey) {
                    item['Sekolah Tujuan'] = app.schoolKey === 'smpn1' ? 'SMPN 1 Bogor' : 'SMPN 3 Bogor';
                }

                item['Status'] = app.isSafe !== false ? 'Aman' : 'Gugur';

                return item;
            });
        }

        function exportCurrentToExcel() {
            if (filteredApplicants.length === 0) {
                alert('Tidak ada data untuk diexport.');
                return;
            }

            const formatted = getFormattedExcelList(filteredApplicants);
            const ws = XLSX.utils.json_to_sheet(formatted);
            const wb = XLSX.utils.book_new();
            
            let sheetName = `${currentSchool.toUpperCase()}_Jalur_${currentPathway}`;
            if (currentPathway === 'prestasi') {
                sheetName = currentSubPathway === 'semua' ? 'Semua Prestasi' :
                            currentSubPathway === 'rapor' ? 'Prestasi Rapor' : 'Prestasi Akademik';
            }
            XLSX.utils.book_append_sheet(wb, ws, sheetName);
            
            const filename = `SPMB_Export_${currentSchool.toUpperCase()}_${currentPathway}_view.xlsx`;
            XLSX.writeFile(wb, filename);
        }

        function exportSchoolToExcel() {
            if (!spmbData) return;
            const wb = XLSX.utils.book_new();
            
            if (currentSchool === 'semua') {
                for (const schoolKey of ['smpn1', 'smpn3']) {
                    const schoolData = spmbData.schools[schoolKey] || {};
                    const pathways = schoolData.pathways || {};
                    const prefix = schoolKey.toUpperCase() + '_';
                    
                    for (const [key, list] of Object.entries(pathways)) {
                        const listWithSchool = list.map(app => ({ ...app, schoolKey }));
                        if (key === 'prestasi') {
                            const wsSemua = XLSX.utils.json_to_sheet(getFormattedExcelList(listWithSchool));
                            XLSX.utils.book_append_sheet(wb, wsSemua, prefix + 'Semua_Prestasi');

                            const raporApps = listWithSchool.filter(app => app.sub_jalur === 'Prestasi Rapor');
                            raporApps.sort((a,b) => (parseFloat(b.nilai_rapor) || 0) - (parseFloat(a.nilai_rapor) || 0));
                            const wsRapor = XLSX.utils.json_to_sheet(getFormattedExcelList(raporApps));
                            XLSX.utils.book_append_sheet(wb, wsRapor, prefix + 'Prestasi_Rapor');

                            const akadApps = listWithSchool.filter(app => app.sub_jalur === 'Prestasi Akademik/Non Akademik');
                            akadApps.sort((a,b) => (parseFloat(b.skor_sertifikat) || 0) - (parseFloat(a.skor_sertifikat) || 0));
                            const wsAkad = XLSX.utils.json_to_sheet(getFormattedExcelList(akadApps));
                            XLSX.utils.book_append_sheet(wb, wsAkad, prefix + 'Prestasi_Akademik');
                        } else {
                            const ws = XLSX.utils.json_to_sheet(getFormattedExcelList(listWithSchool));
                            const nameMap = {
                                'afirmasi': 'Afirmasi',
                                'domisili': 'Domisili',
                                'mutasi': 'Mutasi'
                            };
                            XLSX.utils.book_append_sheet(wb, ws, prefix + (nameMap[key] || key));
                        }
                    }
                }
            } else {
                const schoolData = spmbData.schools[currentSchool] || {};
                const pathways = schoolData.pathways || {};
                
                for (const [key, list] of Object.entries(pathways)) {
                    const listWithSchool = list.map(app => ({ ...app, schoolKey: currentSchool }));
                    if (key === 'prestasi') {
                        const wsSemua = XLSX.utils.json_to_sheet(getFormattedExcelList(listWithSchool));
                        XLSX.utils.book_append_sheet(wb, wsSemua, 'Semua Prestasi');

                        const raporApps = listWithSchool.filter(app => app.sub_jalur === 'Prestasi Rapor');
                        raporApps.sort((a,b) => (parseFloat(b.nilai_rapor) || 0) - (parseFloat(a.nilai_rapor) || 0));
                        const wsRapor = XLSX.utils.json_to_sheet(getFormattedExcelList(raporApps));
                        XLSX.utils.book_append_sheet(wb, wsRapor, 'Prestasi Rapor');

                        const akadApps = listWithSchool.filter(app => app.sub_jalur === 'Prestasi Akademik/Non Akademik');
                        akadApps.sort((a,b) => (parseFloat(b.skor_sertifikat) || 0) - (parseFloat(a.skor_sertifikat) || 0));
                        const wsAkad = XLSX.utils.json_to_sheet(getFormattedExcelList(akadApps));
                        XLSX.utils.book_append_sheet(wb, wsAkad, 'Prestasi Akademik');
                    } else {
                        const ws = XLSX.utils.json_to_sheet(getFormattedExcelList(listWithSchool));
                        const nameMap = {
                            'afirmasi': 'Afirmasi',
                            'domisili': 'Domisili',
                            'mutasi': 'Mutasi'
                        };
                        XLSX.utils.book_append_sheet(wb, ws, nameMap[key] || key);
                    }
                }
            }
            
            const filename = `SPMB_${currentSchool.toUpperCase()}_Full_Data.xlsx`;
            XLSX.writeFile(wb, filename);
        }
    </script>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as out:
        out.write(html_template)
    print("Created index.html (dynamic loader) successfully!")

if __name__ == '__main__':
    main()
