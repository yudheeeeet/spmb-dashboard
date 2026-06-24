import urllib.request
import urllib.parse
import re
import html
import json
from pathlib import Path
from datetime import datetime

def fetch_pathway_data(school_id, jalur):
    base_url = f'https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar/detail/{school_id}'
    url = f'{base_url}?filter=semua&jalur={jalur}&limit=1500&page=1'
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

FALLBACK_SCHOOLS = {
    'smpn1': {'id': '6058e604-2df5-e011-91f0-e9feaa2e9d74', 'name': 'SMP NEGERI 1 BOGOR', 'npsn': '20220385'},
    'smpn2': {'id': '60f12206-2df5-e011-8a46-6bf253e496ab', 'name': 'SMP NEGERI 2', 'npsn': '20220376'},
    'smpn3': {'id': 'e0000704-2df5-e011-842f-5d02e391b0b3', 'name': 'SMP NEGERI 3 BOGOR', 'npsn': '20220377'},
    'smpn4': {'id': '607bb104-2df5-e011-a567-cdd9515cb43f', 'name': 'SMP NEGERI 4 BOGOR', 'npsn': '20220378'},
    'smpn5': {'id': 'f0273e04-2df5-e011-961b-63e7601dc96d', 'name': 'SMP NEGERI 5', 'npsn': '20220379'},
    'smpn6': {'id': '70bb2206-2df5-e011-9597-1d0c912b7fe2', 'name': 'SMP NEGERI 6', 'npsn': '20220380'},
    'smpn7': {'id': '90fc7304-2df5-e011-a95a-a72eb9f84dfc', 'name': 'SMP NEGERI 7 BOGOR', 'npsn': '20220381'},
    'smpn8': {'id': 'e0ebb904-2df5-e011-9694-2bdcdc771da2', 'name': 'SMP NEGERI 8 BOGOR', 'npsn': '20220382'},
    'smpn9': {'id': '50bdf204-2df5-e011-b95c-d9c2a72684e3', 'name': 'SMP NEGERI 9 BOGOR', 'npsn': '20220354'},
    'smpn10': {'id': '20692206-2df5-e011-b8cd-eb0fff6548c8', 'name': 'SMP NEGERI 10 BOGOR', 'npsn': '20220386'},
    'smpn11': {'id': '50d62206-2df5-e011-8b91-5d869f6d3ae8', 'name': 'SMP NEGERI 11 BOGOR', 'npsn': '20220387'},
    'smpn12': {'id': '00d43304-2df5-e011-ad5f-d91be70663ff', 'name': 'SMP NEGERI 12 BOGOR', 'npsn': '20220388'},
    'smpn13': {'id': 'e0762206-2df5-e011-a086-b975477e1497', 'name': 'SMP NEGERI 13 BOGOR', 'npsn': '20220389'},
    'smpn14': {'id': '1012c504-2df5-e011-88b4-8d189dce69ba', 'name': 'SMP NEGERI 14 BOGOR', 'npsn': '20220390'},
    'smpn15': {'id': '5048e004-2df5-e011-9fbe-f373041d48cf', 'name': 'SMP NEGERI 15 BOGOR', 'npsn': '20220391'},
    'smpn16': {'id': '00602306-2df5-e011-8356-59f8c43970df', 'name': 'SMP NEGERI 16', 'npsn': '20220392'},
    'smpn17': {'id': '4049e204-2df5-e011-afcd-97e36bdf92a9', 'name': 'SMP NEGERI 17 BOGOR', 'npsn': '20220384'},
    'smpn18': {'id': '206ae404-2df5-e011-ae3d-9b7426cfeeb7', 'name': 'SMP NEGERI 18 KOTA BOGOR', 'npsn': '20220383'},
    'smpn19': {'id': 'c069ca04-2df5-e011-9836-fda4cfa6b24a', 'name': 'SMP NEGERI 19 BOGOR', 'npsn': '20220375'},
    'smpn20': {'id': 'c02a2306-2df5-e011-b927-093051a2f742', 'name': 'SMP NEGERI 20', 'npsn': '20258321'},
    'smpn21': {'id': '31f1f644-c054-416b-8e24-f25e7cf47b69', 'name': 'SEKOLAH MENENGAH PERTAMA NEGERI 21 BOGOR', 'npsn': '70045813'},
    'smpn22': {'id': '25af2a7f-bd38-4c52-b63c-11a4565cb595', 'name': 'SEKOLAH MENENGAH PERTAMA NEGERI 22 BOGOR', 'npsn': '70054147'},
    'smpn23': {'id': '925de075-6ed1-453b-8fae-e597d0cc0945', 'name': 'SEKOLAH MENENGAH PERTAMA NEGERI 23 BOGOR', 'npsn': '70054148'}
}

def fetch_schools():
    url = 'https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as r:
            html_content = r.read().decode('utf-8')
            match = re.search(r'data-page=\"([^\"]+)\"', html_content)
            if match:
                data = json.loads(html.unescape(match.group(1)))
                schools_data = data.get('props', {}).get('data', [])
                schools = {}
                for item in schools_data:
                    name = item.get('nama_satuan_pendidikan', '')
                    num_match = re.search(r'\d+', name)
                    if num_match:
                        key = f'smpn{num_match.group(0)}'
                    else:
                        key = re.sub(r'[^a-z0-9]', '', name.lower())
                    schools[key] = {
                        'id': item.get('id'),
                        'npsn': item.get('npsn'),
                        'name': name
                    }
                return schools
    except Exception as e:
        print(f'Error fetching schools dynamically: {e}')
    return None

def fetch_pathway_data(school_id, jalur):
    base_url = f'https://spmb.kotabogor.go.id/jenjang-smp/data-spmb/data-pendaftar/detail/{school_id}'
    url = f'{base_url}?filter=semua&jalur={jalur}&limit=1500&page=1'
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

def prune_applicant_data(applicants):
    allowed_keys = {
        'no_pendaftaran',
        'nama_murid',
        'asal_satuan_pendidikan',
        'sub_jalur',
        'nilai_rapor',
        'skor_sertifikat',
        'jarak',
        'status_domisili',
        'skor_akhir'
    }
    pruned = []
    for app in applicants:
        pruned_app = {k: app[k] for k in allowed_keys if k in app}
        if 'sub_jalur' not in pruned_app and 'subJalur' in app:
            pruned_app['sub_jalur'] = app['subJalur']
        pruned.append(pruned_app)
    return pruned

def main():
    schools_config = fetch_schools()
    if not schools_config:
        print('Using fallback static schools config.')
        schools_config = FALLBACK_SCHOOLS
    else:
        print(f'Successfully loaded {len(schools_config)} schools dynamically.')
        
    jalurs = ['afirmasi', 'domisili', 'mutasi', 'prestasi']
    output_data = {
        'last_updated': datetime.now().isoformat(),
        'schools': {}
    }
    
    for key, config in schools_config.items():
        school_id = config['id']
        print(f'Scraping school {key.upper()} ({school_id})...')
        
        school_entry = {
            'info': {
                'id': school_id,
                'nama_satuan_pendidikan': config['name'],
                'npsn': config['npsn'],
                'jumlah_terverifikasi': 0,
                'terakhir_diperbarui': ''
            },
            'pathways': {}
        }
        
        school_info_fetched = False
        
        for jalur in jalurs:
            print(f'  Fetching pathway: {jalur}...')
            props = fetch_pathway_data(school_id, jalur)
            if props:
                raw_apps = props.get('data', [])
                school_entry['pathways'][jalur] = prune_applicant_data(raw_apps)
                if not school_info_fetched:
                    school_info = props.get('satuanPendidikan', {})
                    if school_info:
                        school_entry['info']['nama_satuan_pendidikan'] = school_info.get('nama_satuan_pendidikan', config['name'])
                        school_entry['info']['npsn'] = school_info.get('npsn', config['npsn'])
                        school_entry['info']['jumlah_terverifikasi'] = school_info.get('jumlah_terverifikasi', 0)
                        school_entry['info']['terakhir_diperbarui'] = school_info.get('terakhir_diperbarui', '')
                        school_info_fetched = True
            else:
                school_entry['pathways'][jalur] = []
                
        output_data['schools'][key] = school_entry
        print(f'Completed school {key.upper()}. Total applicants: {school_entry["info"]["jumlah_terverifikasi"]}')
        
    with open('pendaftar_data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print('Scraping run completed successfully. Written to pendaftar_data.json')

if __name__ == '__main__':
    main()
