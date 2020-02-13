from wagtailkit.academic.models import (
    ResourceManagementUnit, CourseType, CourseGroup,
    SchoolYear)


def create_rmu_roots():
    Rmu = ResourceManagementUnit
    dj = Rmu.objects.create(parent=None, name='IBI Darmajaya', number='00', code='IBI', status='1')
    ik = Rmu.objects.create(parent=dj, name='Fakultas Ilmu Komputer', number='10', code='FIK', status='2')
    eb = Rmu.objects.create(parent=dj, name='Fakultas Ekonomi dan Bisnis', number='20', code='FEB', status='2')
    Rmu.objects.create(parent=ik, name='Teknik Informatika', number='11', code='TIP', status='4'),
    Rmu.objects.create(parent=ik, name='Sistem Informasi', number='12', code='SIP', status='4'),
    Rmu.objects.create(parent=ik, name='Sistem Komputer', number='13', code='SKP', status='4'),
    Rmu.objects.create(parent=ik, name='Desain Komunikasi Visual', number='14', code='DKS', status='4'),
    Rmu.objects.create(parent=ik, name='Magister Teknik Informatika', number='15', code='MTI', status='4'),
    Rmu.objects.create(parent=eb, name='Akuntansi', number='21', code='AKS', status='4'),
    Rmu.objects.create(parent=eb, name='Manajemen', number='22', code='EMS', status='4'),
    Rmu.objects.create(parent=eb, name='Bisnis Digital', number='23', code='BDS', status='4'),
    Rmu.objects.create(parent=eb, name='Magister Manajemen', number='24', code='EMM', status='4')


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
        SchoolYear(code='2015/2016', year_start='2015', year_end='2016',),
        SchoolYear(code='2016/2017', year_start='2016', year_end='2017',),
        SchoolYear(code='2017/2018', year_start='2017', year_end='2018',),
        SchoolYear(code='2018/2019', year_start='2018', year_end='2019',),
        SchoolYear(code='2019/2020', year_start='2019', year_end='2020',),
        SchoolYear(code='2020/2021', year_start='2020', year_end='2021',),
        SchoolYear(code='2021/2022', year_start='2021', year_end='2022',),
        SchoolYear(code='2022/2023', year_start='2022', year_end='2023',),
        SchoolYear(code='2023/2024', year_start='2023', year_end='2024',),
        SchoolYear(code='2024/2025', year_start='2024', year_end='2025',)
    ])


def clean_school_year():
    SchoolYear.objects.filter(year_start__in=[
        '2015',
        '2016',
        '2017',
        '2018',
        '2019',
        '2020',
        '2021',
        '2022',
        '2023',
        '2024'
    ]).delete()