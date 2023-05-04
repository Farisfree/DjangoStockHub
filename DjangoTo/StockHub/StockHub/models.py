# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class Collection(models.Model):
    user_id = models.CharField(max_length=15, blank=True, null=True)
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'collection'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class HistoryRecord(models.Model):
    user_id = models.CharField(max_length=15, blank=True, null=True)
    record_secucode = models.CharField(db_column='record_SecuCode', max_length=10, blank=True,
                                       null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'history_record'


class People(models.Model):
    user_id = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.IntegerField(blank=True, null=True)
    account = models.CharField(max_length=15, blank=True, null=True)
    passwd = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class StockBasicInfo(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    compcode = models.IntegerField(db_column='CompCode', blank=True, null=True)  # Field name made lowercase.
    comcd = models.CharField(db_column='Comcd', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stkcd = models.IntegerField(db_column='Stkcd', blank=True, null=True)  # Field name made lowercase.
    lstknm = models.TextField(db_column='Lstknm', blank=True, null=True)  # Field name made lowercase.
    stkcdotrd = models.IntegerField(db_column='Stkcdotrd', blank=True, null=True)  # Field name made lowercase.
    listedstate = models.CharField(db_column='Listedstate', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    csrciccd1 = models.CharField(db_column='Csrciccd1', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    csrciccd2 = models.CharField(db_column='Csrciccd2', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_basic_info'


class StockDailyData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    date_field = models.DateField(db_column='Date_', blank=True,
                                  null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    prevclpr = models.FloatField(db_column='PrevClPr', blank=True, null=True)  # Field name made lowercase.
    oppr = models.FloatField(db_column='Oppr', blank=True, null=True)  # Field name made lowercase.
    hipr = models.FloatField(db_column='Hipr', blank=True, null=True)  # Field name made lowercase.
    lopr = models.FloatField(db_column='Lopr', blank=True, null=True)  # Field name made lowercase.
    clpr = models.FloatField(db_column='Clpr', blank=True, null=True)  # Field name made lowercase.
    adjclpr1 = models.FloatField(db_column='AdjClpr1', blank=True, null=True)  # Field name made lowercase.
    adjclpr2 = models.FloatField(db_column='AdjClpr2', blank=True, null=True)  # Field name made lowercase.
    trdvol = models.FloatField(db_column='Trdvol', blank=True, null=True)  # Field name made lowercase.
    trdsum = models.FloatField(db_column='Trdsum', blank=True, null=True)  # Field name made lowercase.
    dampltd = models.FloatField(db_column='Dampltd', blank=True, null=True)  # Field name made lowercase.
    dfulturnr = models.FloatField(db_column='DFulTurnR', blank=True, null=True)  # Field name made lowercase.
    dtrdturnr = models.FloatField(db_column='DTrdTurnR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_daily_data'


class StockDividendData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    exdt = models.DateField(db_column='Exdt', blank=True, null=True)  # Field name made lowercase.
    dividend = models.FloatField(db_column='Dividend', blank=True, null=True)  # Field name made lowercase.
    stksprate = models.FloatField(db_column='Stksprate', blank=True, null=True)  # Field name made lowercase.
    shrcmprsrate = models.FloatField(db_column='Shrcmprsrate', blank=True, null=True)  # Field name made lowercase.
    stkdrate = models.FloatField(db_column='Stkdrate', blank=True, null=True)  # Field name made lowercase.
    capissurate = models.FloatField(db_column='Capissurate', blank=True, null=True)  # Field name made lowercase.
    snipr = models.FloatField(db_column='Snipr', blank=True, null=True)  # Field name made lowercase.
    snivol = models.FloatField(db_column='Snivol', blank=True, null=True)  # Field name made lowercase.
    rigoffrate = models.FloatField(db_column='Rigoffrate', blank=True, null=True)  # Field name made lowercase.
    rigoffpr = models.FloatField(db_column='Rigoffpr', blank=True, null=True)  # Field name made lowercase.
    arigoffshr = models.FloatField(db_column='Arigoffshr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_dividend_data'


class StockFeesData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    coma = models.FloatField(db_column='Coma', blank=True, null=True)  # Field name made lowercase.
    comb = models.FloatField(db_column='Comb', blank=True, null=True)  # Field name made lowercase.
    stamptaxa = models.FloatField(db_column='Stamptaxa', blank=True, null=True)  # Field name made lowercase.
    stamptaxb = models.FloatField(db_column='Stamptaxb', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_fees_data'


class StockFinancialData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    infopubdt = models.DateField(db_column='Infopubdt', blank=True, null=True)  # Field name made lowercase.
    enddt = models.DateField(db_column='Enddt', blank=True, null=True)  # Field name made lowercase.
    reporttype = models.CharField(db_column='Reporttype', max_length=2, blank=True,
                                  null=True)  # Field name made lowercase.
    eps = models.FloatField(db_column='EPS', blank=True, null=True)  # Field name made lowercase.
    roe = models.FloatField(db_column='ROE', blank=True, null=True)  # Field name made lowercase.
    accumfundps = models.FloatField(db_column='AccumFundPS', blank=True, null=True)  # Field name made lowercase.
    opprfps = models.FloatField(db_column='OpPrfPS', blank=True, null=True)  # Field name made lowercase.
    naps = models.FloatField(db_column='NAPS', blank=True, null=True)  # Field name made lowercase.
    napsadj = models.FloatField(db_column='NAPSadj', blank=True, null=True)  # Field name made lowercase.
    incomeps = models.FloatField(db_column='IncomePS', blank=True, null=True)  # Field name made lowercase.
    ncffropeps = models.FloatField(db_column='NCFfropePS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_financial_data'


class StockPriceData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    pcash = models.FloatField(db_column='Pcash', blank=True, null=True)  # Field name made lowercase.
    pshrrate = models.FloatField(db_column='Pshrrate', blank=True, null=True)  # Field name made lowercase.
    pshrrate_c = models.FloatField(db_column='Pshrrate_C', blank=True, null=True)  # Field name made lowercase.
    pshrrate_s = models.FloatField(db_column='Pshrrate_S', blank=True, null=True)  # Field name made lowercase.
    pcapissurate = models.FloatField(db_column='Pcapissurate', blank=True, null=True)  # Field name made lowercase.
    mcfacpr = models.FloatField(db_column='Mcfacpr', blank=True, null=True)  # Field name made lowercase.
    qttncurrency = models.CharField(db_column='Qttncurrency', max_length=5, blank=True,
                                    null=True)  # Field name made lowercase.
    ex = models.FloatField(db_column='Ex', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_price_data'


class StockRatiosData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    pe = models.FloatField(db_column='PE', blank=True, null=True)  # Field name made lowercase.
    pb = models.FloatField(db_column='PB', blank=True, null=True)  # Field name made lowercase.
    pcf = models.FloatField(db_column='PCF', blank=True, null=True)  # Field name made lowercase.
    ps = models.FloatField(db_column='PS', blank=True, null=True)  # Field name made lowercase.
    date_field = models.DateField(db_column='Date_', blank=True,
                                  null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'stock_ratios_data'


class StockReturnData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    date_field = models.DateField(db_column='Date_', blank=True,
                                  null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    dret = models.FloatField(db_column='Dret', blank=True, null=True)  # Field name made lowercase.
    daret = models.FloatField(db_column='Daret', blank=True, null=True)  # Field name made lowercase.
    dreteq = models.FloatField(db_column='Dreteq', blank=True, null=True)  # Field name made lowercase.
    drettmv = models.FloatField(db_column='Drettmv', blank=True, null=True)  # Field name made lowercase.
    dretmc = models.FloatField(db_column='Dretmc', blank=True, null=True)  # Field name made lowercase.
    dareteq = models.FloatField(db_column='Dareteq', blank=True, null=True)  # Field name made lowercase.
    darettmv = models.FloatField(db_column='Darettmv', blank=True, null=True)  # Field name made lowercase.
    daretmc = models.FloatField(db_column='Daretmc', blank=True, null=True)  # Field name made lowercase.
    drfret = models.FloatField(db_column='DRfRet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_return_data'


class StockSharesData(models.Model):
    secucode = models.CharField(db_column='SecuCode', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    capchgdt = models.DateField(db_column='Capchgdt', blank=True, null=True)  # Field name made lowercase.
    comstateshr = models.FloatField(db_column='Comstateshr', blank=True, null=True)  # Field name made lowercase.
    comlpshr = models.FloatField(db_column='Comlpshr', blank=True, null=True)  # Field name made lowercase.
    fullshr = models.FloatField(db_column='Fullshr', blank=True, null=True)  # Field name made lowercase.
    trdshr = models.FloatField(db_column='Trdshr', blank=True, null=True)  # Field name made lowercase.
    lsttrdshr = models.FloatField(db_column='Lsttrdshr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_shares_data'
