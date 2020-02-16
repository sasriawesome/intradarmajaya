from django.db import transaction
from wagtailkit.organizations.models import Department, Position

def import_department_and_position():
    with transaction.atomic():
        dept = Department.objects
        rektorat = dept.create(parent=None, name='Rektorat IBI Darmajaya', code='rektorat-ibi-darmajaya')
        rektorat_1 = dept.create(parent=rektorat, name='Rektorat Bidang Akademik dan Riset',
                                 code='rekbid-akademik-riset')
        rektorat_2 = dept.create(parent=rektorat, name='Rektorat Bidang Sumberdaya', code='rekbid-sumberdaya')
        rektorat_3 = dept.create(parent=rektorat, name='Rektorat Bidang Kemahasiswaan & Inkubator',
                                 code='rekbid-kemahasiswaan')
        rektorat_4 = dept.create(parent=rektorat, name='Rektorat Bidang Pengembangan dan Pemasaran',
                                 code='rekbid-pengembangan')

        # Jajaran Rektorat 1

        fak_ilkom = dept.create(parent=rektorat_1, name='Fakultas Ilmu Komputer', code='fakultas-ilmu-komputer')
        jur_ti = dept.create(parent=fak_ilkom, name='Jurusan Teknik Informatika', code='jurusan-ti')
        kbk_ti = dept.create(parent=jur_ti, name='KBK Teknik Informatika', code='kbk-ti')
        jur_si = dept.create(parent=fak_ilkom, name='Jurusan Sistem Informasi', code='jurusan-si')
        kbk_si = dept.create(parent=jur_si, name='KBK Sistem Informasi', code='kbk-si')
        jur_sk = dept.create(parent=fak_ilkom, name='Jurusan Sistem Komputer', code='jurusan-sk')
        kbk_sk = dept.create(parent=jur_sk, name='KBK Sistem Komputer', code='kbk-sk')
        jur_dkv = dept.create(parent=fak_ilkom, name='Jurusan Desain Komunikasi Visual', code='jurusan-dkv')
        kbk_dkv = dept.create(parent=jur_dkv, name='KBK Desain Komunikasi Visual', code='kbk-dkv')
        prod_mti = dept.create(parent=fak_ilkom, name='Prodi Magister Teknik Informatika', code='jurusan-mti')
        kbk_mti = dept.create(parent=prod_mti, name='KBK Magister Teknik Informatika', code='kbk-mti')

        fak_ekbis = dept.create(parent=rektorat_1, name='Fakultas Ekonomi dan Bisnis',
                                code='fakultas-ekonomi-dan-bisnis')
        jur_ak = dept.create(parent=fak_ekbis, name='Jurusan Akuntansi', code='jurusan-akt')
        kbk_ak = dept.create(parent=jur_ak, name='KBK Akuntansi', code='kbk-ak')
        jur_ma = dept.create(parent=fak_ekbis, name='Jurusan Manajemen', code='jurusan-mnj')
        kbk_ma = dept.create(parent=jur_ma, name='KBK Manajemen', code='kbk-ma')
        jur_bi = dept.create(parent=fak_ekbis, name='Jurusan Bisnis Digital', code='jurusan-bisnis_digital')
        kbk_bi = dept.create(parent=jur_bi, name='KBK Bisnis Digital', code='kbk-bi')
        prodi_mm = dept.create(parent=fak_ekbis, name='Prodi Magister Manajemen', code='prodi-bi')
        kbk_mm = dept.create(parent=prodi_mm, name='KBK Magister Manajemen', code='kbk-mm')

        laboratorium = dept.create(parent=rektorat_1, name='Laboratorium', code='laboratorium')
        lp4m = dept.create(parent=rektorat_1, name='Lembaga Pengembangan Pembelajaran (LP4m)', code='lp4m')
        pus_haki = dept.create(parent=lp4m, name='Pusat HAKI dan Publikasi', code='pus-haki')
        pus_bangjar = dept.create(parent=lp4m, name='Pusat Pengembangan Pembelajaran', code='pus-bangjar')
        pus_penelitian = dept.create(parent=lp4m, name='Pusat Penelitian', code='pus-pe-nelitian')
        pus_pengabdian = dept.create(parent=lp4m, name='Pusat Pengabdian Masyarakat', code='pus-pengabdian')

        baak = dept.create(parent=rektorat_1, name='BAAK', code='baak')
        pus_regak = dept.create(parent=baak, name='Pusat Registrasi Akdemik', code='pus-registrasi')
        plpp = dept.create(parent=baak, name='Pusat Layanan Pelaporan dan Perkuliahan (PLPP)', code='plpp')

        pus_pelatihan = dept.create(parent=rektorat_1, name='Pusat Pelatihan', code='pus-dik-lat')
        pus_bahasa = dept.create(parent=rektorat_1, name='Pusat Bahasa', code='pusat-bahasa')
        pus_perpustakaan = dept.create(parent=rektorat_1, name='Perpustakaan', code='perpustakaan')
        ict_center = dept.create(parent=rektorat_1, name='Biro ICT Center', code='ict-center')
        bag_jaringan = dept.create(parent=ict_center, name='Bagian Jaringan', code='bag-jaringan')
        bag_software = dept.create(parent=ict_center, name='Bagian Analis & Programmer', code='bag-software')

        # Jajaran Rektorat 2

        biro_keuangan = dept.create(parent=rektorat_2, name='Biro Keuangan', code='biro-keuangan')
        bag_adm_akuntansi = dept.create(parent=biro_keuangan, name='Bagian Akuntansi', code='bag-akuntansi')
        bag_adm_keuangan = dept.create(parent=biro_keuangan, name='Bagian Keuangan', code='bag-keuangan')
        biro_asset_logistik = dept.create(parent=rektorat_2, name='Biro Manajemen Asset dan Logistik',
                                          code='biro-asset-logistik')
        bag_asset_logistik = dept.create(parent=biro_asset_logistik, name='Bagian Asset dan Inventori',
                                         code='bag-asset')
        bag_perawatan = dept.create(parent=biro_asset_logistik, name='Bagian Pengelolaan, Perawatan, Keamanan',
                                    code='bag-perawatan')
        biro_sdm = dept.create(parent=rektorat_2, name='Biro Sumber Daya Manusia', code='biro-sdm')
        bag_payroll_recruitment = dept.create(parent=biro_sdm, name='Bagian Payroll dan Recruitment',
                                              code='bag-pay-recruit')
        bag_banglat = dept.create(parent=biro_sdm, name='Bagian Pengembangan dan Pelatihan', code='bag-bang-latih')

        # Jajaran Rektorat 3

        satgas_budaya = dept.create(parent=rektorat_3, name='Satgas Budaya', code='satgas_budaya')
        biro_pembinaan = dept.create(parent=rektorat_3, name='Biro Pembinaan, Kemahasiswaan dan Karakter',
                                     code='biro-pembinaan')
        bag_ki_k = dept.create(parent=biro_pembinaan, name='Bagian Kegiatan Intrakurikuler dan Kemahasiswaan',
                               code='biro-kik')
        bag_ke_a = dept.create(parent=biro_pembinaan, name='Bagian Kegiatan Extrakurikuler dan Alumni', code='biro-kea')
        bag_pemkar = dept.create(parent=biro_pembinaan, name='Bagian Pembinaan Karakter', code='biro-binakar')
        biro_inkubator = dept.create(parent=rektorat_3, name='Biro Inkubator, Career Center dan Rumah Tangga',
                                     code='biro-inkubator')
        rt_protokoler = dept.create(parent=biro_inkubator, name='Bagian Inkubator dan Protokoler', code='rt-protokoler')
        inkubator_career_center = dept.create(parent=biro_inkubator, name='Bagian Inkubator dan Career Center',
                                              code='inkubator-career-center')

        # Jajaran Rektorat 4

        lemlapor_jamintu = dept.create(parent=rektorat_4, name='Lembaga Pelaporan dan Penjaminan Mutu',
                                       code='lemlapor-jamintu')
        bag_qad = dept.create(parent=lemlapor_jamintu, name='Bagian Quality Assurance dan Designer', code='biro-qad')
        bag_agmi = dept.create(parent=lemlapor_jamintu, name='Bagian AGMI', code='biro-agmi')
        biro_humas_pemasaran = dept.create(parent=rektorat_4, name='Biro Humas, Kerjasama dan Pemasaran',
                                           code='humas-pemasaran')
        international = dept.create(parent=biro_humas_pemasaran, name='Bagian Hubungan Internasional',
                                    code='hub-internasional')
        kehumasan = dept.create(parent=biro_humas_pemasaran, name='Bagian Kehumasan', code='bag-humas')
        pemasaran = dept.create(parent=biro_humas_pemasaran, name='Bagian Pemasaran', code='bag-pemasaran')
        kerjasama = dept.create(parent=biro_humas_pemasaran, name='Bagian Kerjasama', code='bag-kerjasama')

        # POSITION
        # -------------------------------------------------------------------------------------------------------------

        chair = Position.objects.create
        rektor = chair(parent=None, department=rektorat, name='Rektor', is_manager=True)
        # Warek I
        warek_1 = chair(parent=rektor, department=rektorat_1, name='Wakil Rektor 1', is_manager=True)
        dekan_fik = chair(parent=warek_1, department=fak_ilkom, name='Dekan FIK', is_manager=True)
        wakil_dekan_fik = chair(parent=dekan_fik, department=fak_ilkom, name='Wakil Dekan FIK', is_manager=False,
                                is_co_manager=True)
        kajur_ti = chair(parent=wakil_dekan_fik, department=jur_ti, name='Kepala Jurusan TI', is_manager=True)
        sekjur_ti = chair(parent=kajur_ti, department=jur_ti, name='Sekretaris Jurusan TI', is_manager=False)
        kajur_si = chair(parent=wakil_dekan_fik, department=jur_si, name='Kepala Jurusan SI', is_manager=True)
        sekjur_si = chair(parent=kajur_si, department=jur_si, name='Sekretaris Jurusan SI', is_manager=False)
        kajur_sk = chair(parent=wakil_dekan_fik, department=jur_sk, name='Kepala Jurusan SK', is_manager=True)
        sekjur_sk = chair(parent=kajur_sk, department=jur_sk, name='Sekretaris Jurusan SK', is_manager=False)
        kajur_dkv = chair(parent=wakil_dekan_fik, department=jur_dkv, name='Kepala Jurusan DKV', is_manager=True)
        sekjur_dkv = chair(parent=kajur_dkv, department=jur_dkv, name='Sekretaris Jurusan DKV', is_manager=False)
        kaprodi_mti = chair(parent=wakil_dekan_fik, department=prod_mti, name='Kepala Prodi MTI', is_manager=True)

        dekan_feb = chair(parent=warek_1, department=fak_ilkom, name='Dekan FEB', is_manager=True)
        wakil_dekan_feb = chair(parent=dekan_feb, department=fak_ekbis, name='Wakil Dekan FEB', is_co_manager=True)
        kajur_ak = chair(parent=wakil_dekan_feb, department=jur_ak, name='Kepala Jurusan Akuntansi', is_manager=True)
        sekjur_ak = chair(parent=kajur_ak, department=jur_ak, name='Sekretaris Jurusan AKT', is_manager=False)
        kajur_ma = chair(parent=wakil_dekan_feb, department=jur_ma, name='Kepala Jurusan Manajemen', is_manager=True)
        sekjur_ma = chair(parent=kajur_ma, department=jur_ma, name='Sekretaris Jurusan MAN', is_manager=False)
        kajur_bi = chair(parent=wakil_dekan_feb, department=jur_bi, name='Kepala Jurusan Bisnis Digital',
                         is_manager=True)
        sekjur_bi = chair(parent=kajur_bi, department=jur_bi, name='Sekretaris Jurusan BDG', is_manager=False)
        kaprodi_mm = chair(parent=wakil_dekan_feb, department=prodi_mm, name='Kepala Prodi MM', is_manager=True)

        kabiro_ict = chair(parent=warek_1, department=ict_center, name='Kepala Biro ICT', is_manager=True)
        kabag_jaringan = chair(parent=kabiro_ict, department=bag_jaringan, name='Kepala Bagian Jarkom', is_manager=True)
        kabag_analis = chair(parent=kabiro_ict, department=bag_software, name='Kepala Analis & Programmer',
                             is_manager=True)

        ka_lp4m = chair(parent=warek_1, department=lp4m, name='Kepala LP4M', is_manager=True)
        kapus_haki = chair(parent=ka_lp4m, department=pus_haki, name='Kepala Pusat HAKI', is_manager=True)
        staff_haki = chair(parent=kapus_haki, department=pus_haki, name='Staff Pusat HAKI')
        kapus_bangjar = chair(parent=ka_lp4m, department=pus_bangjar, name='Kepala Pusat Pengembangan Pembelajaran',
                              is_manager=True)
        staff_bangjar = chair(parent=kapus_bangjar, department=pus_bangjar,
                              name='Staff Pusat Pengembangan Pembelajaran')
        kapus_penelitian = chair(parent=ka_lp4m, department=pus_penelitian, name='Kepala Pusat Penelitian',
                                 is_manager=True)
        staff_penelitian = chair(parent=kapus_penelitian, department=pus_penelitian, name='Staff Pusat Penelitian')
        kapus_pengabdian = chair(parent=ka_lp4m, department=pus_pengabdian, name='Kepala Pusat Pengabdian Masyarakat',
                                 is_manager=True)
        staff_pus_pengabdian = chair(parent=kapus_pengabdian, department=pus_pengabdian,
                                     name='Staff Pusat Pengabdian Masyarakat')

        kabiro_baak = chair(parent=warek_1, department=baak, name='Kepala BAAK', is_manager=True)
        kabag_regak = chair(parent=kabiro_baak, department=pus_regak, name='Kepala Bagian R&A', is_manager=True)
        staff_regak = chair(parent=kabag_regak, department=pus_regak, name='Staff Bagian R&A')
        kabag_plpp = chair(parent=kabiro_baak, department=plpp, name='Kepala Bagian PLPP', is_manager=True)
        staff_plpp = chair(parent=kabag_plpp, department=plpp, name='Staff PLPP')
        koordinator_laboran = chair(parent=warek_1, department=laboratorium, name='Koordinator Laboratorium',
                                    is_manager=True)
        laboran = chair(parent=koordinator_laboran, department=laboratorium, name='Laboran', is_manager=True)

        kapus_pelatihan = chair(parent=warek_1, department=pus_pelatihan, name='Kepala Pusat Pelatihan',
                                is_manager=True)
        staff_pelatihan = chair(parent=kapus_penelitian, department=pus_pelatihan, name='Staff Pusat Pelatihan')
        kapus_bahasa = chair(parent=warek_1, department=pus_bahasa, name='Kepala Pusat Bahasa', is_manager=True)
        staff_bahasa = chair(parent=kapus_bahasa, department=pus_bahasa, name='Staff Pusat Bahasa')
        kapus_perpustakaan = chair(parent=warek_1, department=pus_perpustakaan, name='Kepala Pusat Perpustakaan',
                                   is_manager=True)
        staff_perpustakaan = chair(parent=kapus_perpustakaan, department=pus_perpustakaan, name='Staff Perpustakaan')

        warek_2 = chair(parent=rektor, department=rektorat_2, name='Wakil Rektor 2', is_manager=True)
        kabiro_keuangan = chair(parent=warek_2, department=biro_keuangan, name='Kepala Biro Administrasi Keuangan',
                                is_manager=True)
        kabak_adm_keu = chair(parent=kabiro_keuangan, department=bag_adm_keuangan,
                              name='Kepala Bagian Administrasi Keuangan', is_manager=True)
        kabak_akuntansi = chair(parent=kabiro_keuangan, department=bag_adm_akuntansi,
                                name='Kepala Bagian Administrasi Akuntansi', is_manager=True)
        kabiro_mal = chair(parent=warek_2, department=biro_asset_logistik, name='Kepala Biro Asset dan Logistik',
                           is_manager=True)
        kabag_asset_logistik = chair(parent=kabiro_mal, department=bag_asset_logistik,
                                     name='Kepala Bagian Inventaris & Logistik', is_manager=True)
        kabag_perawatan = chair(parent=kabiro_mal, department=bag_perawatan,
                                name='Kepala Bagian Pengelolaan, Perawatan, Keamanan', is_manager=True)
        kabiro_sdm = chair(parent=warek_2, department=biro_sdm, name='Kepala Biro SDM', is_manager=True)
        kabag_payroll_recruitment = chair(parent=kabiro_sdm, department=bag_payroll_recruitment,
                                          name='Kepala Bagian Payroll & Recruitment', is_manager=True)
        kabag_banglat = chair(parent=kabiro_sdm, department=bag_banglat, name='Kepala Bagian Pengembangan & Pelatihan',
                              is_manager=True)

        warek_3 = chair(parent=rektor, department=rektorat_3, name='Wakil Rektor 3', is_manager=True)
        kabiro_pembinaan = chair(parent=warek_3, department=biro_pembinaan,
                                 name='Kepala Biro Pembinaan Kemahasiswaan & Karakter', is_manager=True)
        kabag_ki_k = chair(parent=kabiro_pembinaan, department=bag_ki_k, name='Kepala Bagian KI & K', is_manager=True)
        kabag_ke_a = chair(parent=kabiro_pembinaan, department=bag_ke_a, name='Kepala Bagian KE & A', is_manager=True)
        kabag_pembinaan_karakter = chair(parent=kabiro_pembinaan, department=bag_pemkar,
                                         name='Kepala Bagian Pembinaan Karakter', is_manager=True)
        kabiro_inkubator = chair(parent=warek_3, department=biro_inkubator,
                                 name='Kepala Biro Inkubator, Karir Center, RT', is_manager=True)
        kabag_rt = chair(parent=kabiro_inkubator, department=rt_protokoler, name='Kepala Bagian RT & Protokoler',
                         is_manager=True)
        kabag_inkubator = chair(parent=kabiro_inkubator, department=inkubator_career_center,
                                name='Kepala Bagian Inkubator', is_manager=True)

        warek_4 = chair(parent=rektor, department=rektorat_4, name='Wakil Rektor 4', is_manager=True)
        kalemlapor_jamintu = chair(parent=warek_4, department=lemlapor_jamintu, name='Kepala Biro LPMP',
                                   is_manager=True)
        kabag_qad = chair(parent=kalemlapor_jamintu, department=bag_qad, name='Kepala QAD', is_manager=True)
        kabag_agmi = chair(parent=kalemlapor_jamintu, department=bag_agmi, name='Kepala AGMI', is_manager=True)
        kabiro_humas_pemasaran = chair(parent=warek_4, department=biro_humas_pemasaran, name='Kepala Biro HKPI',
                                       is_manager=True)
        kabag_international = chair(parent=kabiro_humas_pemasaran, department=international,
                                    name='Kepala Bagian Kantor HI', is_manager=True)
        kabag_pemasaran = chair(parent=kabiro_humas_pemasaran, department=pemasaran, name='Kepala Bagian Pemasaran',
                                is_manager=True)
        kabag_kehumasan = chair(parent=kabiro_humas_pemasaran, department=kehumasan, name='Kepala Bagian Kehumasan',
                                is_manager=True)
        kabag_kerjasama = chair(parent=kabiro_humas_pemasaran, department=kerjasama, name='Kepala Bagian Kerjasama',
                                is_manager=True)

        dosen_ti = chair(parent=kajur_ti, department=kbk_ti, name='Dosen TI', is_manager=False)
        dosen_si = chair(parent=kajur_si, department=kbk_si, name='Dosen SI', is_manager=False)
        dosen_sk = chair(parent=kajur_sk, department=kbk_sk, name='Dosen SK', is_manager=False)
        dosen_dkv = chair(parent=kajur_dkv, department=kbk_dkv, name='Dosen DKV', is_manager=False)
        dosen_mti = chair(parent=kaprodi_mti, department=kbk_mti, name='Dosen MTI', is_manager=False)
        dosen_ak = chair(parent=kajur_ak, department=kbk_ak, name='Dosen Akuntansi', is_manager=False)
        dosen_ma = chair(parent=kajur_ma, department=kbk_ma, name='Dosen Manajemen', is_manager=False)
        dosen_bi = chair(parent=kajur_bi, department=kbk_bi, name='Dosen Bisnis Digital', is_manager=False)
        dosen_mm = chair(parent=kaprodi_mm, department=kbk_mm, name='Dosen Magister Manajemen', is_manager=False)
