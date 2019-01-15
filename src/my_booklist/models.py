from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.timezone import now


class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)

    author1 = models.CharField(max_length=50)
    author2 = models.CharField(max_length=50, blank=True, null=True)
    author3 = models.CharField(max_length=50, blank=True, null=True)
    author4 = models.CharField(max_length=200, blank=True, null=True)

    add_date = models.DateTimeField(default=now)

    isbn_regex = RegexValidator(regex=r'^[0-9]+$')
    isbn = models.CharField(validators=[isbn_regex, MinLengthValidator(10)],
                            max_length=13, unique=True)

    NUMERICAL_CALCULATION = 'nc'
    SOLID_STATE_PHYSICS = 'ss'
    QUANTUM_FIELD_THEORY = 'qf'
    ELECTROMAGNETISM = 'em'
    ANALYTICAL_MECHANICS = 'am'
    PHYSICS = 'ph'
    STATISTICAL_MECHANICS = 'sm'
    QUANTUM_MECHANICS = 'qm'
    QUANTUM_OPTICS = 'qo'
    QUANTUM_INFORMATION = 'qi'
    QUANTUM_PHYSICS = 'qp'
    PROBABILITY_PROCESS = 'pp'
    MATHEMATICS = 'mt'
    OTHERS = 'ot'

    CATEGORY_CHOICES = (
        (QUANTUM_MECHANICS, '量子力学(qm)'),
        (QUANTUM_OPTICS, '量子光学(qo)'),
        (QUANTUM_INFORMATION, '量子情報(qi)'),
        (QUANTUM_PHYSICS, '量子物理学(qp)'),
        (QUANTUM_FIELD_THEORY, '場の量子論(qf)'),
        (SOLID_STATE_PHYSICS, '固体物理学・超伝導(ss)'),
        (STATISTICAL_MECHANICS, '統計力学(sm)'),
        (ELECTROMAGNETISM, '電磁気学(em)'),
        (ANALYTICAL_MECHANICS, '力学・解析力学(am)'),
        (PHYSICS, '物理学一般(ph)'),
        (PROBABILITY_PROCESS, '確率過程(pp)'),
        (NUMERICAL_CALCULATION, '計算機・数値計算(nc)'),
        (MATHEMATICS, '数学(mt)'),
        (OTHERS, 'その他(ot)')
    )
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES
    )

    rent_flag = models.BooleanField(
        default=False
    )
    rent_user = models.CharField(max_length=50, blank=True, null=True)
    rent_date = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        return self.title
