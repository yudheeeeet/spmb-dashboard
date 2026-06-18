[Objective]
Tambahkan fitur visual berupa "Garis Batas Kuota" (Cut-off Line / Passing Grade Line) pada tabel daftar urutan siswa di dashboard klasemen penerimaan. Garis ini berfungsi untuk memisahkan siswa yang masuk dalam kuota penerimaan dan siswa yang berada di luar kuota pada masing-masing sekolah dan jalur.

[Context & Data Available]

Tabel siswa saat ini sudah menampilkan: Nama Siswa, Skor, Nilai Rapor (TK), Wilayah, dan Waktu Pendaftaran.

Data kuota per jalur (Domisili, Afirmasi, Prestasi, Mutasi) untuk masing-masing sekolah sudah tersedia di database (berasal dari link referensi kuota).

[Logic & Requirements]

1. Logika Garis Batas Jalur Domisili:

Ambil data kuota Domisili untuk sekolah yang sedang dilihat (Contoh: SMP 1 kuota Domisili = 130).

Pastikan tabel sudah terurut (sorted) secara otomatis berdasarkan prioritas: Wilayah (Wilayah 1 di atas, disusul wilayah selanjutnya) lalu berdasarkan ketentuan sekunder (misal: waktu pendaftaran).

Sisipkan garis horizontal tebal (sebagai indikator passing grade) tepat di bawah baris data siswa ke-{X}, di mana {X} adalah jumlah kuota Domisili. (Contoh: Garis muncul di bawah siswa urutan ke-130).

2. Logika Garis Batas Jalur Prestasi:

Ambil data total kuota Prestasi untuk sekolah yang sedang dilihat (Contoh: SMP 1 kuota Prestasi = 97).

Karena jalur Prestasi terbagi menjadi dua sub-jalur (Jalur Rapor dan Jalur Akademis/Non-Akademis), bagi total kuota tersebut sesuai proporsi regulasi (misal dibagi rata: 48 untuk Rapor, 49 untuk Akademis/Non-Akademis).

Pada tab/tabel Prestasi Rapor: Sisipkan garis batas di bawah baris data siswa ke-{Y} (Contoh: di bawah siswa urutan ke-48).

Pada tab/tabel Prestasi Akademis/Non-Akademis: Sisipkan garis batas di bawah baris data siswa ke-{Z} (Contoh: di bawah siswa urutan ke-49).

[UI/UX Notes]

Buat desain garis pemisah cukup menonjol (misalnya warna merah atau abu-abu tebal) dengan teks kecil di tengah/samping garis bertuliskan: "Batas Kuota Terpenuhi".

Siswa yang berada di bawah garis dapat diberikan indikator visual tambahan (misalnya warna baris sedikit diredupkan/ dimmed) untuk mempertegas bahwa mereka saat ini berada di luar kuota aman.