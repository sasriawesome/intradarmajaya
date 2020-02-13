import datetime
from django.utils import timezone
from wagtailkit.academic.models import (
    ResourceManagementUnit, CourseType, CourseGroup,
    SchoolYear, AcademicYear, Curriculum, Course, CurriculumCourse)


def create_rmu_roots():
    Rmu = ResourceManagementUnit
    ibi = Rmu.objects.create(parent=None, name='IBI Darmajaya', number='00', code='IBI', status='1')
    fik = Rmu.objects.create(parent=ibi, name='Fakultas Ilmu Komputer', number='10', code='FIK', status='2')
    feb = Rmu.objects.create(parent=ibi, name='Fakultas Ekonomi dan Bisnis', number='20', code='FEB', status='2')
    tip = Rmu.objects.create(parent=fik, name='Teknik Informatika', number='11', code='TIP', status='4')
    sip = Rmu.objects.create(parent=fik, name='Sistem Informasi', number='12', code='SIP', status='4')
    skp = Rmu.objects.create(parent=fik, name='Sistem Komputer', number='13', code='SKP', status='4')
    dks = Rmu.objects.create(parent=fik, name='Desain Komunikasi Visual', number='14', code='DKS', status='4')
    mti = Rmu.objects.create(parent=fik, name='Magister Teknik Informatika', number='15', code='MTI', status='4')
    aks = Rmu.objects.create(parent=feb, name='Akuntansi', number='21', code='AKS', status='4')
    ems = Rmu.objects.create(parent=feb, name='Manajemen', number='22', code='EMS', status='4')
    bds = Rmu.objects.create(parent=feb, name='Bisnis Digital', number='23', code='BDS', status='4')
    emm = Rmu.objects.create(parent=feb, name='Magister Manajemen', number='24', code='EMM', status='4')


def clean_rmu_roots():
    ResourceManagementUnit.objects.filter(code__in=[
        'IBI', 'FIK', 'FEB', 'TIP', 'SIP', 'SKP', 'DKS', 'MTI', 'AKS', 'EMS', 'BDS', 'EMM'
    ]).delete()


def create_course_type():
    CourseType.objects.bulk_create([
        CourseType(code='1', name='Wajib', alias='A'),
        CourseType(code='2', name='Pilihan', alias='B'),
        CourseType(code='3', name='Peminatan', alias='C'),
        CourseType(code='4', name='Tugas akhir / Skripsi /Thesis / Disertasi', alias='D'),
    ])


def clean_course_type():
    CourseType.objects.filter(code__in=['1', '2', '3', '4']).delete()


def create_course_group():
    CourseGroup.objects.bulk_create([
        CourseGroup(code='1', name='Mata Kuliah Umum / Mata Kuliah Dasar Umum', alias='MKDU'),
        CourseGroup(code='2', name='Mata Kuliah Dasar Keahlian', alias='MKDK'),
        CourseGroup(code='3', name='Mata Kuliah Keilmuan dan Keterampilan', alias='MKK'),
        CourseGroup(code='4', name='Mata Kuliah Keahlian Berkarya', alias='MKB'),
        CourseGroup(code='5', name='Mata Kuliah Perilaku Berkarya', alias='MPB'),
        CourseGroup(code='6', name='Mata Kuliah Pengembangan Kepribadian', alias='MPK'),
        CourseGroup(code='7', name='Mata Kuliah Berkehidupan Bermasyarakat', alias='MBB'),
    ])


def clean_course_group():
    CourseGroup.objects.filter(code__in=['1', '2', '3', '4', '5', '6', '7']).delete()


def create_school_year():
    SchoolYear.objects.bulk_create([
        # SchoolYear(code='2015/2016', year_start=2015, year_end=2016, ),
        # SchoolYear(code='2016/2017', year_start=2016, year_end=2017, ),
        # SchoolYear(code='2017/2018', year_start=2017, year_end=2018, ),
        # SchoolYear(code='2018/2019', year_start=2018, year_end=2019, ),
        SchoolYear(code='2019/2020', year_start=2019, year_end=2020, ),
        SchoolYear(code='2020/2021', year_start=2020, year_end=2021, ),
        # SchoolYear(code='2021/2022', year_start=2021, year_end=2022, ),
        # SchoolYear(code='2022/2023', year_start=2022, year_end=2023, ),
        # SchoolYear(code='2023/2024', year_start=2023, year_end=2024, ),
        # SchoolYear(code='2024/2025', year_start=2024, year_end=2025, )
    ])


def clean_school_year():
    SchoolYear.objects.filter(
        year_start__in=[
            2015, 2016, 2017, 2018, 2019,
            2020, 2021, 2022, 2023, 2024
        ]).delete()


def create_academic_year():
    school_year_2019 = SchoolYear.objects.get(year_start=2019)
    school_year_2020 = SchoolYear.objects.get(year_start=2020)
    # school_year_2021 = SchoolYear.objects.get(year_start=2021)
    AcademicYear(
        school_year=school_year_2019,
        semester=AcademicYear.ODD,
        date_start=timezone.make_aware(timezone.datetime(2019, 6, 1)),
        date_end=timezone.make_aware(timezone.datetime(2020, 9, 30))
    )
    AcademicYear(
        school_year=school_year_2019,
        semester=AcademicYear.EVEN,
        date_start=timezone.make_aware(timezone.datetime(2019, 12, 1)),
        date_end=timezone.make_aware(timezone.datetime(2020, 5, 30))
    )
    AcademicYear(
        school_year=school_year_2020,
        semester=AcademicYear.ODD,
        date_start=timezone.make_aware(timezone.datetime(2020, 6, 1)),
        date_end=timezone.make_aware(timezone.datetime(2021, 9, 30))
    )
    AcademicYear(
        school_year=school_year_2020,
        semester=AcademicYear.EVEN,
        date_start=timezone.make_aware(timezone.datetime(2021, 12, 1)),
        date_end=timezone.make_aware(timezone.datetime(2021, 5, 30))
    )
    # AcademicYear(
    #     school_year=school_year_2021,
    #     semester=AcademicYear.ODD,
    #     date_start=timezone.make_aware(timezone.datetime(2021, 6, 1)),
    #     date_end=timezone.make_aware(timezone.datetime(2021, 9, 30))
    # )
    # AcademicYear(
    #     school_year=school_year_2021,
    #     semester=AcademicYear.EVEN,
    #     date_start=timezone.make_aware(timezone.datetime(2021, 12, 1)),
    #     date_end=timezone.make_aware(timezone.datetime(2022, 5, 30))
    # )


def clean_academic_year():
    AcademicYear.objects.all().delete()


def create_curriculum():
    rmu_tip = ResourceManagementUnit.objects.get(code='TIP')
    rmu_sip = ResourceManagementUnit.objects.get(code='SIP')
    rmu_skp = ResourceManagementUnit.objects.get(code='SKP')
    rmu_mti = ResourceManagementUnit.objects.get(code='MTI')
    rmu_aks = ResourceManagementUnit.objects.get(code='AKS')
    rmu_ems = ResourceManagementUnit.objects.get(code='EMS')
    rmu_bds = ResourceManagementUnit.objects.get(code='BDS')
    rmu_emm = ResourceManagementUnit.objects.get(code='EMM')
    Curriculum.objects.bulk_create([
        Curriculum(code='TIP2019', year='2019', rmu=rmu_tip, name='Teknik Informatika 2019', sks_graduate=144),
        Curriculum(code='SIP2019',year='2019', rmu=rmu_sip, name='Sistem Informasi 2019', sks_graduate=144),
        # Curriculum(code='SKP2019',year='2019', rmu=rmu_skp, name='Sistem Komputer 2019', sks_graduate=144),
        # Curriculum(code='MTI2019',year='2019', rmu=rmu_mti, name='Magister Teknik Informatika 2019', sks_graduate=94),
        # Curriculum(code='AKS2019',year='2019', rmu=rmu_aks, name='Akuntansi 2019', sks_graduate=144),
        # Curriculum(code='EMS2019',year='2019', rmu=rmu_ems, name='Manajemen 2019', sks_graduate=144),
        # Curriculum(code='BDS2019',year='2019', rmu=rmu_bds, name='Bisnis Digital 2019', sks_graduate=144),
        # Curriculum(code='EMM2019',year='2019', rmu=rmu_emm, name='Magister Manajemen 2019', sks_graduate=94)
    ])


def clean_curriculum():
    Curriculum.objects.all().delete()


def create_course():

    # Univesity and Faculty
    rmu_ibi = ResourceManagementUnit.objects.get(code='IBI')
    rmu_fik = ResourceManagementUnit.objects.get(code='FIK')
    rmu_feb = ResourceManagementUnit.objects.get(code='FEB')

    # Program Study
    rmu_tip = ResourceManagementUnit.objects.get(code='TIP')
    rmu_sip = ResourceManagementUnit.objects.get(code='SIP')
    rmu_skp = ResourceManagementUnit.objects.get(code='SKP')
    rmu_mti = ResourceManagementUnit.objects.get(code='MTI')
    rmu_aks = ResourceManagementUnit.objects.get(code='AKS')
    rmu_ems = ResourceManagementUnit.objects.get(code='EMS')
    rmu_bds = ResourceManagementUnit.objects.get(code='BDS')
    rmu_emm = ResourceManagementUnit.objects.get(code='EMM')

    wajib = CourseType.objects.get(code='1')
    pilihan = CourseType.objects.get(code='2')
    peminatan = CourseType.objects.get(code='3')
    penelitian = CourseType.objects.get(code='4')

    mkdu = CourseGroup.objects.get(alias='MKDU')
    mkdk = CourseGroup.objects.get(alias='MKDK')
    mkk = CourseGroup.objects.get(alias='MKK')
    mkb = CourseGroup.objects.get(alias='MKB')
    mpk = CourseGroup.objects.get(alias='MPB')

    # IBI Course
    agama = Course.objects.create(rmu=rmu_ibi, name='Agama', teaching_method='Teori', course_type=wajib, course_group=mkdu, level='6',year_offered=1)
    agama_budha = Course.objects.create(rmu=rmu_ibi, name='Agama Budha', teaching_method='Teori', course_type=wajib, course_group=mkdu, level='6',year_offered=1)
    agama_hindu = Course.objects.create(rmu=rmu_ibi, name='Agama Hindu', teaching_method='Teori', course_type=wajib, course_group=mkdu, level='6', year_offered=1)
    agama_protestan = Course.objects.create(rmu=rmu_ibi, name='Agama Protestan', teaching_method='Teori', course_type=wajib, course_group=mkdu, level='6', year_offered=1)
    agama_katolik = Course.objects.create(rmu=rmu_ibi, name='Agama Katolik', teaching_method='Teori', course_type=wajib, course_group=mkdu, level='6', year_offered=1)
    kewarganegaraan = Course.objects.create(rmu=rmu_ibi, name='Kewarganegaraan', teaching_method='Teori', course_type=wajib, course_group=mkdu, level='6', year_offered=1)

    # FIK Course
    dasar2_arsitektur_komputer = Course.objects.create(rmu=rmu_fik, name='Dasar - Dasar Arsitektur Komputer', year_offered=1, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    prinsip2_sistem_informasi = Course.objects.create(rmu=rmu_fik, name='Prinsip - Prinsip Sistem Informasi', year_offered=1, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    matematika_dasar = Course.objects.create(rmu=rmu_fik, name='Matematika Dasar', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=1)
    fisika_dasar = Course.objects.create(rmu=rmu_fik, name='Fisika Dasar', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=1)
    matematika_diskrit = Course.objects.create(rmu=rmu_fik, name='Matematika Diskret 1', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=1)
    matematika_diskrit_2 = Course.objects.create(rmu=rmu_fik, name='Matematika Diskret 2', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    aljabar_linear = Course.objects.create(rmu=rmu_fik, name='Aljabar Linier', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    statistika = Course.objects.create(rmu=rmu_fik, name='Statistika dan Probabilitas', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    dasar2_pemrograman = Course.objects.create(rmu=rmu_fik, name='Dasar-Dasar Pemrograman 1', teaching_method='Praktik', course_type=wajib, course_group=mkdk, level='6', year_offered=1)
    dasar2_pemrograman2 = Course.objects.create(rmu=rmu_fik, name='Dasar-Dasar Pemrograman 2', teaching_method='Praktik', course_type=wajib, course_group=mkdk, level='6', year_offered=1)
    pemrograman_web = Course.objects.create(rmu=rmu_fik, name='Perancangan & Pemrograman Web', teaching_method='Praktik dan Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    struktur_data = Course.objects.create(rmu=rmu_fik, name='Struktur Data & Algoritma', teaching_method='Praktik dan Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    sistem_operasi = Course.objects.create(rmu=rmu_fik, name='Sistem Operasi', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    basis_data = Course.objects.create(rmu=rmu_fik, name='Basis Data', teaching_method='Praktik dan Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=2)
    metode_penelitian = Course.objects.create(rmu=rmu_fik, name='Metodologi Penelitian & Penulisan Ilmiah', teaching_method='Teori', course_type=penelitian, course_group=mkdk, level='6', year_offered=3)
    kerja_praktik = Course.objects.create(rmu=rmu_fik, name='Kerja Praktik', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=4)
    manusia_dan_komputer = Course.objects.create(rmu=rmu_fik, name='Manusia dan Komputer', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=4)
    tugas_akhir = Course.objects.create(rmu=rmu_fik, name='Tugas Akhir', teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6', year_offered=4)

    # TI Course Wajib
    pengantar_sistem_dijital = Course.objects.create(rmu=rmu_tip, name='Pengantar Sistem Dijital', year_offered=1, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    pengantar_organisasi_komputer = Course.objects.create(rmu=rmu_tip, name='Pengantar Organisasi Komputer', year_offered=1, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    matematika_dasar2 = Course.objects.create(rmu=rmu_tip, name='Matematika Dasar 2', year_offered=1, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    pemrograman_lanjut = Course.objects.create(rmu=rmu_tip, name='Pemrograman Lanjut', year_offered=2, teaching_method='Praktik', course_type=wajib, course_group=mkdk, level='6')
    teori_bahasa_automata = Course.objects.create(rmu=rmu_tip, name='Teori Bahasa & Automata', year_offered=2, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    rekayasa_perangkat_lunak = Course.objects.create(rmu=rmu_tip, name='Rekayasa Perangkat Lunak', year_offered=2, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    pemrograman_sistem = Course.objects.create(rmu=rmu_tip, name='Pemrograman Sistem', year_offered=3, teaching_method='Praktik', course_type=wajib, course_group=mkdk, level='6')
    sistem_cerdas = Course.objects.create(rmu=rmu_tip, name='Sistem Cerdas', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    jaringan_komputer = Course.objects.create(rmu=rmu_tip, name='Jaringan Komputer', year_offered=3, teaching_method='Praktik', course_type=wajib, course_group=mkdk, level='6')
    proyek_perangkat_lunak = Course.objects.create(rmu=rmu_tip, name='Proyek Perangkat Lunak', year_offered=3, teaching_method='Praktik', course_type=wajib, course_group=mkdk, level='6')
    data_science = Course.objects.create(rmu=rmu_tip, name='Data Science & Analytics', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    analisis_numerik = Course.objects.create(rmu=rmu_tip, name='Analisis Numerik', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    desain_algoritma = Course.objects.create(rmu=rmu_tip, name='Desain & Analisis Algoritma', year_offered=4, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')

    # TIP Pilihan
    basis_data_lanjut = Course.objects.create(rmu=rmu_tip, name='Basis Data Lanjut', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    teknik_kompilator = Course.objects.create(rmu=rmu_tip, name='Teknik Kompilator', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    grafika_komputer = Course.objects.create(rmu=rmu_tip, name='Grafika Komputer', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    kriptografi = Course.objects.create(rmu=rmu_tip, name='Kriptografi & Keamanan Informasi', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    layanan_web = Course.objects.create(rmu=rmu_tip, name='Layanan & Aplikasi Web', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    pemrograman_paralel = Course.objects.create(rmu=rmu_tip, name='Pemrograman Paralel', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    teknologi_mobile = Course.objects.create(rmu=rmu_tip, name='Teknologi Mobile', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    pm_perangkat_lunak = Course.objects.create(rmu=rmu_tip, name='Penjaminan Mutu Perangkat Lunak', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    penambangan_data = Course.objects.create(rmu=rmu_tip, name='Penambangan Data', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')

    # SIP Course Wajib
    administrasi_bisnis = Course.objects.create(rmu=rmu_sip, name='Administrasi Bisnis', year_offered=2, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    prinsip_manajemen = Course.objects.create(rmu=rmu_sip, name='Prinsip - Prinsip Manajemen', year_offered=2, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    sistem_perusahaan  = Course.objects.create(rmu=rmu_sip, name='Sistem - Sistem Perusahaan', year_offered=2, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    sia_keuangan = Course.objects.create(rmu=rmu_sip, name='Sistem Informasi Akuntansi dan Keuangan', year_offered=2, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    sistem_interaksi = Course.objects.create(rmu=rmu_sip, name='Sistem Interaksi', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    analisis_perancangan_si = Course.objects.create(rmu=rmu_sip, name='Analisis dan Perancangan Sistem Informasi', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    arsitektur_aplikasi_keuangan = Course.objects.create(rmu=rmu_sip, name='Arsitektur & Pemrograman Aplikasi Perusahaan', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    manpro_ti = Course.objects.create(rmu=rmu_sip, name='Manajemen Proyek TI', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    jarkom_data = Course.objects.create(rmu=rmu_sip, name='Jaringan Komunikasi Data', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    proyek_pengembangan_si = Course.objects.create(rmu=rmu_sip, name='Proyek Pengembangan Sistem Informasi', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    komunikasi_bisnis_teknis = Course.objects.create(rmu=rmu_sip, name='Komunikasi Bisnis dan Teknis', year_offered=3, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    statistika_si = Course.objects.create(rmu=rmu_sip, name='Statistika Terapan', year_offered=4, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')
    manajemen_si = Course.objects.create(rmu=rmu_sip, name='Manajemen Sistem Informasi', year_offered=4, teaching_method='Teori', course_type=wajib, course_group=mkdk, level='6')

    # SIP Pilihan
    manajemen_layanan_ti = Course.objects.create(rmu=rmu_sip, name='Manajemen Layanan TI', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    administrasi_sistem = Course.objects.create(rmu=rmu_sip, name='Administrasi Sistem', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    manajemen_infrastruktur_ti = Course.objects.create(rmu=rmu_sip, name='Manajemen Infrastruktur TI', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    technopreneurship =Course(rmu=rmu_sip, name='Technopreneurship', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    teknologi_mobile = Course.objects.create(rmu=rmu_sip, name='Teknologi Mobile', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    pengantar_keamanan_si = Course.objects.create(rmu=rmu_sip, name='Pengantar Keamanan Informasi', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    perangkat_lunak_opensource = Course.objects.create(rmu=rmu_sip, name='Pengembangan Perangkat Lunak Open Source', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    integrasi_aplikasi_perusahaan = Course.objects.create(rmu=rmu_sip, name='Integrasi Aplikasi Perusahaan', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    dasar2_audit_si = Course.objects.create(rmu=rmu_sip, name='Dasar - Dasar Audit SI', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')
    manajemen_infrastruktur_si = Course.objects.create(rmu=rmu_sip, name='Manajemen Infrastruktur SI / TI', year_offered=4, teaching_method='Teori', course_type=pilihan, course_group=mkdk, level='6')

    curriculum_ti = Curriculum.objects.get(code='TIP2019')

    # TI Semester I 24 SKS
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=agama, semester_number='1', semester_type='1', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=kewarganegaraan, semester_number='1', semester_type='1', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=prinsip2_sistem_informasi, semester_number='1', semester_type='1', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=matematika_dasar, semester_number='1', semester_type='1', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=fisika_dasar, semester_number='1', semester_type='1', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=dasar2_pemrograman, semester_number='1', semester_type='1', sks_meeting=0, sks_practice=4),
    ])

    # TI Semester II 22
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=pengantar_sistem_dijital, semester_number='2', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=matematika_dasar2, semester_number='2', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=dasar2_pemrograman2, semester_number='2', semester_type='2', sks_meeting=0, sks_practice=6),
        CurriculumCourse(curriculum=curriculum_ti, course=pengantar_organisasi_komputer, semester_number='2', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=dasar2_arsitektur_komputer, semester_number='2', semester_type='2', sks_meeting=3, sks_practice=4),
    ])

    # TI Semester III 22
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=matematika_diskrit, semester_number='3', semester_type='1', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=aljabar_linear, semester_number='3', semester_type='1', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=basis_data, semester_number='3', semester_type='1', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=teori_bahasa_automata, semester_number='3', semester_type='1', sks_meeting=0, sks_practice=6),
        CurriculumCourse(curriculum=curriculum_ti, course=struktur_data, semester_number='3', semester_type='1', sks_meeting=3, sks_practice=4),
    ])

    # TI Semester IV 22
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=matematika_diskrit_2, semester_number='4', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=statistika, semester_number='4', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=rekayasa_perangkat_lunak, semester_number='4', semester_type='2', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=pemrograman_web, semester_number='4', semester_type='2', sks_meeting=0, sks_practice=6),
        CurriculumCourse(curriculum=curriculum_ti, course=sistem_operasi, semester_number='4', semester_type='2', sks_meeting=3, sks_practice=0),
    ])

    # TI Semester V
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=pemrograman_sistem, semester_number='5', semester_type='1',sks_meeting=6, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=jaringan_komputer, semester_number='5', semester_type='1', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=kerja_praktik, semester_number='5', semester_type='1', sks_meeting=2, sks_practice=8),
        CurriculumCourse(curriculum=curriculum_ti, course=data_science, semester_number='5', semester_type='1', sks_meeting=4, sks_practice=0),
    ])

    # TI Semester VI 22
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=proyek_perangkat_lunak, semester_number='6', semester_type='1', sks_meeting=0, sks_practice=6),
        CurriculumCourse(curriculum=curriculum_ti, course=sistem_cerdas, semester_number='6', semester_type='2',sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=pemrograman_lanjut, semester_number='6', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=analisis_numerik, semester_number='6', semester_type='2', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=teknologi_mobile, semester_number='6', semester_type='2', sks_meeting=0, sks_practice=4),
    ])

    # TI Semester VII
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=desain_algoritma, semester_number='7', semester_type='1', sks_meeting=3, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=metode_penelitian, semester_number='7', semester_type='1', sks_meeting=6, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=basis_data_lanjut, semester_number='7', semester_type='1', sks_meeting=0, sks_practice=4),
        CurriculumCourse(curriculum=curriculum_ti, course=teknik_kompilator, semester_number='7', semester_type='1', sks_meeting=0, sks_practice=4),
    ])

    # TI Semester VIII 20
    CurriculumCourse.objects.bulk_create([
        CurriculumCourse(curriculum=curriculum_ti, course=manusia_dan_komputer, semester_number='8', semester_type='2', sks_meeting=4, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=tugas_akhir, semester_number='8', semester_type='2', sks_meeting=8, sks_practice=0),
        CurriculumCourse(curriculum=curriculum_ti, course=layanan_web, semester_number='8', semester_type='2', sks_meeting=0, sks_practice=4),
    ])

    for course in Course.objects.all():
        course.save()

    for curriculum_course in CurriculumCourse.objects.all():
        curriculum_course.save()

def clean_course():
    Course.objects.all().delete()