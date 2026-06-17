import urllib.request
import urllib.parse
import re
import html
import json
import sys
from pathlib import Path

def fetch_jalur_data(school_id, jalur):
    base_url = f'https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar/detail/{school_id}'
    url = f'{base_url}?filter=semua&jalur={jalur}&limit=300&page=1' # limit 300 to capture all pendaftar (SMPN 3 has 207 max in Domisili)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        match = re.search(r'data-page=\"([^\"]+)\"', html_content)
        if match:
            data = json.loads(html.unescape(match.group(1)))
            return data.get('props', {})
        else:
            print(f'Warning: data-page not found for {school_id} - {jalur}')
            return None
    except Exception as e:
        print(f'Error fetching {school_id} - {jalur}:', e)
        return None

def scrape_school(school_id, prefix):
    raw_dir = Path('./raw')
    raw_dir.mkdir(exist_ok=True)
    
    jalurs = ['afirmasi', 'domisili', 'mutasi', 'prestasi']
    
    # Fetch initial to get school info
    first_props = fetch_jalur_data(school_id, 'mutasi')
    if not first_props:
        print(f'Error: Could not retrieve initial data for {school_id}.')
        return
        
    school = first_props.get('satuanPendidikan', {})
    school_name = school.get('nama_satuan_pendidikan', 'SMP NEGERI')
    npsn = school.get('npsn', 'UNKNOWN')
    jumlah_terverifikasi = school.get('jumlah_terverifikasi', 0)
    last_update = school.get('terakhir_diperbarui', '')
    
    print(f'Processing School: {school_name} ({prefix.upper()}) (NPSN: {npsn})')
    print(f'Total Verified: {jumlah_terverifikasi}')
    
    # Fetch all pathways
    all_props = {}
    for jalur in jalurs:
        print(f'  Fetching {jalur}...')
        props = fetch_jalur_data(school_id, jalur)
        if props:
            all_props[jalur] = props
            
    # Write overview file
    overview_content = f"""---
source_url: "https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar/detail/{school_id}"
type: document
title: "{school_name} Overview"
---

# {school_name} - SPMB Bogor 2026

## School Information
- **Name**: {school_name}
- **NPSN**: {npsn}
- **Total Verified Applicants**: {jumlah_terverifikasi}
- **Last Updated**: {last_update}
- **UUID**: {school_id}

## Admission Pathways Summary
"""
    
    total_pendaftar_per_jalur = first_props.get('totalPendaftarPerJalur', {})
    for k, v in total_pendaftar_per_jalur.items():
        overview_content += f"- **{v.get('nama')}**: {v.get('total')} applicants\n"
        if 'subjalur_options' in v:
            overview_content += "  - Sub-pathways:\n"
            for opt in v['subjalur_options']:
                if opt.get('value'):
                    overview_content += f"    - {opt.get('label')} (code: {opt.get('value')})\n"
                    
    overview_file = raw_dir / f'{prefix}_overview.md'
    with open(overview_file, 'w', encoding='utf-8') as f:
        f.write(overview_content)
    print(f'  Created {overview_file}')
    
    # Write each pathway to its own file
    for jalur in jalurs:
        props = all_props.get(jalur)
        if not props:
            continue
            
        applicants = props.get('data', [])
        pathway_info = props.get('totalPendaftarPerJalur', {}).get(jalur, {})
        pathway_name = pathway_info.get('nama', jalur.capitalize())
        
        md_content = f"""---
source_url: "https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar/detail/{school_id}?filter=semua&jalur={jalur}&limit=300&page=1"
type: document
title: "Jalur {pathway_name} - {school_name}"
---

# Jalur {pathway_name} - {school_name}

This page contains the list of applicants registered under the **{pathway_name}** pathway for {school_name}.

## Summary
- **Pathway Name**: {pathway_name}
- **Total Applicants**: {len(applicants)}

## Applicants List

| No. Pendaftaran | Nama Murid | Asal Sekolah (Origin School) | Sub Jalur | Nilai Rapor | Jarak (m) | Skor Sertifikat | Status Domisili | Skor Akhir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
        for app in applicants:
            no_pendaftaran = app.get('no_pendaftaran', '-')
            nama_murid = app.get('nama_murid', '-')
            asal_sekolah = app.get('asal_satuan_pendidikan', '-')
            sub_jalur = app.get('sub_jalur', '-')
            nilai_rapor = app.get('nilai_rapor', '-')
            jarak = app.get('jarak', '-')
            skor_sertifikat = app.get('skor_sertifikat', '-')
            status_domisili = app.get('status_domisili', '-')
            skor_akhir = app.get('skor_akhir', '-')
            
            md_content += f"| {no_pendaftaran} | {nama_murid} | {asal_sekolah} | {sub_jalur} | {nilai_rapor} | {jarak} | {skor_sertifikat} | {status_domisili} | {skor_akhir} |\n"
            
        filename = f'{prefix}_pathway_{jalur}.md'
        with open(raw_dir / filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f'  Created {filename} with {len(applicants)} applicants')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python scrape_school_to_md.py <school_uuid> <prefix>")
        sys.exit(1)
    scrape_school(sys.argv[1], sys.argv[2])
