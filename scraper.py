import urllib.request
import urllib.parse
import re
import html
import json
from pathlib import Path
from datetime import datetime

def fetch_pathway_data(school_id, jalur):
    base_url = f'https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar/detail/{school_id}'
    url = f'{base_url}?filter=semua&jalur={jalur}&limit=300&page=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        match = re.search(r'data-page=\"([^\"]+)\"', html_content)
        if match:
            data = json.loads(html.unescape(match.group(1)))
            return data.get('props', {})
    except Exception as e:
        print(f'Error fetching {school_id} - {jalur}: {e}')
    return None

def main():
    schools_config = {
        'smpn1': {
            'id': '6058e604-2df5-e011-91f0-e9feaa2e9d74',
            'name_default': 'SMP NEGERI 1 BOGOR'
        },
        'smpn3': {
            'id': 'e0000704-2df5-e011-842f-5d02e391b0b3',
            'name_default': 'SMP NEGERI 3 BOGOR'
        }
    }
    
    jalurs = ['afirmasi', 'domisili', 'mutasi', 'prestasi']
    output_data = {
        'last_updated': datetime.now().isoformat(),
        'schools': {}
    }
    
    for key, config in schools_config.items():
        school_id = config['id']
        print(f'Scraping school {key.upper()} ({school_id})...')
        
        # Initial fetch to get metadata
        init_props = fetch_pathway_data(school_id, 'mutasi')
        if not init_props:
            print(f'Failed to fetch initial data for {key}. Skipping.')
            continue
            
        school_info = init_props.get('satuanPendidikan', {})
        school_name = school_info.get('nama_satuan_pendidikan', config['name_default'])
        npsn = school_info.get('npsn', 'UNKNOWN')
        jumlah_terverifikasi = school_info.get('jumlah_terverifikasi', 0)
        terakhir_diperbarui = school_info.get('terakhir_diperbarui', '')
        
        school_entry = {
            'info': {
                'id': school_id,
                'nama_satuan_pendidikan': school_name,
                'npsn': npsn,
                'jumlah_terverifikasi': jumlah_terverifikasi,
                'terakhir_diperbarui': terakhir_diperbarui
            },
            'pathways': {}
        }
        
        for jalur in jalurs:
            print(f'  Fetching pathway: {jalur}...')
            props = fetch_pathway_data(school_id, jalur)
            if props:
                school_entry['pathways'][jalur] = props.get('data', [])
            else:
                school_entry['pathways'][jalur] = []
                
        output_data['schools'][key] = school_entry
        print(f'Completed school {key.upper()}. Total applicants: {jumlah_terverifikasi}')
        
    with open('pendaftar_data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print('Scraping run completed successfully. Written to pendaftar_data.json')

if __name__ == '__main__':
    main()
