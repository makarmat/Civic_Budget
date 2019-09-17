from django.db import models

# Create your models here.

REGION = (
    ('', 'wybierz subregion'),
    (1, 'jeleniogórski'),
    (2, 'legnicki'),
    (3, 'wałbrzyski'),
    (4, 'wrocławski'),
    (5, 'm. Wrocław')
)

SUBJECT = (
    ('', 'wybierz obszar merytoryczny'),
    (1, 'sport'),
    (2, 'turystyka'),
    (3, 'kultura'),
    (4, 'wsparcie osób z niepełnosprawnościami'),
    (5, 'wsparcie społeczeństwa obywatelskiego'),
    (6, 'wsparcie seniorów'),
    (7, 'wsparcie rzemiosła')
)

VERIFIED = (
    ('', ''),
    (0, 'negatywna'),
    (1, 'pozytywna')
)


class Originator(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Imię')
    last_name = models.CharField(max_length=64, verbose_name='Nazwisko')
    pesel = models.CharField(max_length=11, verbose_name='PESEL')
    phone = models.IntegerField(verbose_name='Numer telefonu')
    email = models.EmailField(max_length=64, verbose_name='E-mail')
    post_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=256, verbose_name='Tytuł wniosku')
    start_date = models.DateField(verbose_name='Data ropoczęcia')
    end_date = models.DateField(verbose_name='Data zakończenia')
    region = models.IntegerField(choices=REGION, verbose_name='Subregion')
    subject = models.IntegerField(choices=SUBJECT, verbose_name='Obszar merytoryczny')
    description_short = models.TextField(max_length=1000,
                                         verbose_name='Skrócony opis projektu (max. 1000 znków ze spacjami)')
    description_long = models.TextField(max_length=2000,
                                        verbose_name='Opis projektu (max. 2000 znków ze spacjami)')
    originator = models.OneToOneField(Originator, on_delete=models.CASCADE, related_name='project_originator')
    applied = models.BooleanField(default=False)
    comment = models.TextField(verbose_name='Uwagi', null=True, blank=True)
    verified = models.IntegerField(verbose_name='Weryfikacja formalna', choices=VERIFIED, null=True, blank=True)
    votes = models.PositiveIntegerField(default=0)

    @property
    def nr_name(self):
        return '{}. {}'.format(self.id, self.name)

    def __str__(self):
        return self.nr_name


class Cost(models.Model):
    cost_name = models.CharField(max_length=64, verbose_name='Nazwa kosztu')
    grant_cost = models.FloatField(verbose_name='Koszt z dotacji (w zł)')
    other_cost = models.FloatField(verbose_name='Finansowanie z innych źródeł (w zł)')
    whole_cost = models.FloatField()
    originator = models.ForeignKey(Originator, on_delete=models.CASCADE, related_name='cost_originator')


class Voter(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Imię')
    last_name = models.CharField(max_length=64, verbose_name='Nazwisko')
    pesel = models.CharField(max_length=11, verbose_name='PESEL')
    phone = models.IntegerField(verbose_name='Numer telefonu')
    email = models.EmailField(max_length=64, verbose_name='E-mail')
    post_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.name


