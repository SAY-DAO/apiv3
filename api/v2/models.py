# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    activitycode = models.IntegerField(db_column='activityCode')  # Field name made lowercase.
    id_social_worker = models.ForeignKey('SocialWorker', models.DO_NOTHING, db_column='id_social_worker')
    diff = models.JSONField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activity'


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ChangeCost(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    need = models.ForeignKey('Need', models.DO_NOTHING)
    requester = models.ForeignKey('SocialWorker', models.DO_NOTHING, related_name='maded_change_cost')
    reviewer = models.ForeignKey('SocialWorker', models.DO_NOTHING, blank=True, null=True, related_name='reveiewed_change_cost')
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_field = models.IntegerField(db_column='from_')  # Field renamed because it ended with '_'.
    to = models.IntegerField()
    description = models.CharField(max_length=128)
    reject_cause = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'change_cost'


class Child(models.Model):
    phonenumber = models.CharField(db_column='phoneNumber', max_length=1000)  # Field name made lowercase.
    nationality = models.CharField(max_length=1000, blank=True, null=True)
    awakeavatarurl = models.CharField(db_column='awakeAvatarUrl', max_length=1000)  # Field name made lowercase.
    housingstatus = models.CharField(db_column='housingStatus', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    familycount = models.IntegerField(db_column='familyCount', blank=True, null=True)  # Field name made lowercase.
    education = models.CharField(max_length=1000, blank=True, null=True)
    birthplace = models.TextField(db_column='birthPlace', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    voiceurl = models.CharField(db_column='voiceUrl', max_length=1000)  # Field name made lowercase.
    id_ngo = models.ForeignKey('Ngo', models.DO_NOTHING, db_column='id_ngo')
    id_social_worker = models.ForeignKey('SocialWorker', models.DO_NOTHING, db_column='id_social_worker')
    confirmuser = models.IntegerField(db_column='confirmUser', blank=True, null=True)  # Field name made lowercase.
    confirmdate = models.DateField(db_column='confirmDate', blank=True, null=True)  # Field name made lowercase.
    generatedcode = models.CharField(db_column='generatedCode', max_length=1000)  # Field name made lowercase.
    city = models.IntegerField()
    country = models.IntegerField()
    gender = models.BooleanField()
    birthdate = models.DateField(db_column='birthDate', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    isconfirmed = models.BooleanField(db_column='isConfirmed')  # Field name made lowercase.
    sayfamilycount = models.IntegerField(db_column='sayFamilyCount')  # Field name made lowercase.
    ismigrated = models.BooleanField(db_column='isMigrated')  # Field name made lowercase.
    migratedid = models.IntegerField(db_column='migratedId', blank=True, null=True)  # Field name made lowercase.
    migratedate = models.DateField(db_column='migrateDate', blank=True, null=True)  # Field name made lowercase.
    sleptavatarurl = models.TextField(db_column='sleptAvatarUrl')  # Field name made lowercase.
    bio_summary_translations = models.TextField(blank=True, null=True)  # This field type is a guess.
    bio_translations = models.TextField(blank=True, null=True)  # This field type is a guess.
    sayname_translations = models.TextField(blank=True, null=True)  # This field type is a guess.
    firstname_translations = models.TextField(db_column='firstName_translations', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastname_translations = models.TextField(db_column='lastName_translations', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    created = models.DateTimeField()
    updated = models.DateTimeField()
    existence_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'child'


class ChildMigration(models.Model):
    child = models.ForeignKey(Child, models.DO_NOTHING)
    new_sw = models.ForeignKey('SocialWorker', models.DO_NOTHING, related_name='new_sw')
    old_sw = models.ForeignKey('SocialWorker', models.DO_NOTHING, related_name='old_sw')
    new_generated_code = models.CharField(max_length=1000)
    old_generated_code = models.CharField(max_length=1000)
    migrated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'child_migration'


class ChildNeed(models.Model):
    id_need = models.ForeignKey('Need', models.DO_NOTHING, db_column='id_need')
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    id_child = models.ForeignKey(Child, models.DO_NOTHING, db_column='id_child')
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'child_need'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Family(models.Model):
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    id_child = models.ForeignKey(Child, models.DO_NOTHING, db_column='id_child')
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'family'


class InvitationAccepts(models.Model):
    invtee = models.ForeignKey('User', models.DO_NOTHING)
    invitation = models.ForeignKey('Invitations', models.DO_NOTHING)
    created = models.DateTimeField()
    role = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invitation_accepts'


class Invitations(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    family = models.ForeignKey(Family, models.DO_NOTHING)
    role = models.IntegerField(blank=True, null=True)
    token = models.CharField(unique=True, max_length=128)
    see_count = models.IntegerField()
    text = models.CharField(max_length=512, blank=True, null=True)
    inviter = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invitations'


class NakamaOwners(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    address = models.CharField(primary_key=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'nakama_owners'


class NakamaTxs(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    id = models.CharField(primary_key=True, max_length=120)
    sender_address = models.ForeignKey(NakamaOwners, models.DO_NOTHING, db_column='sender_address', blank=True, null=True)
    need = models.ForeignKey('Need', models.DO_NOTHING, blank=True, null=True)
    value = models.BigIntegerField(blank=True, null=True)
    is_confirmed = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nakama_txs'


class Need(models.Model):
    imageurl = models.CharField(db_column='imageUrl', max_length=1000)  # Field name made lowercase.
    category = models.IntegerField()
    field_cost = models.IntegerField(db_column='_cost')  # Field renamed because it started with '_'.
    affiliatelinkurl = models.CharField(db_column='affiliateLinkUrl', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    receipts = models.CharField(max_length=1000, blank=True, null=True)
    confirmdate = models.DateTimeField(db_column='confirmDate', blank=True, null=True)  # Field name made lowercase.
    confirmuser = models.IntegerField(db_column='confirmUser', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    isconfirmed = models.BooleanField(db_column='isConfirmed')  # Field name made lowercase.
    type = models.IntegerField()
    isurgent = models.BooleanField(db_column='isUrgent')  # Field name made lowercase.
    child = models.ForeignKey(Child, models.DO_NOTHING, blank=True, null=True)
    doing_duration = models.IntegerField()
    details = models.TextField(blank=True, null=True)
    doneat = models.DateTimeField(db_column='doneAt', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField()
    link = models.TextField(blank=True, null=True)
    isreported = models.BooleanField(db_column='isReported', blank=True, null=True)  # Field name made lowercase.
    ngo_delivery_date = models.DateTimeField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    oncepurchased = models.BooleanField(db_column='oncePurchased')  # Field name made lowercase.
    purchase_date = models.DateTimeField(blank=True, null=True)
    child_delivery_date = models.DateTimeField(blank=True, null=True)
    expected_delivery_date = models.DateTimeField(blank=True, null=True)
    description_translations = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_translations = models.TextField(blank=True, null=True)  # This field type is a guess.
    status_updated_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    purchase_cost = models.IntegerField()
    bank_track_id = models.CharField(max_length=30, blank=True, null=True)
    unavailable_from = models.DateTimeField(blank=True, null=True)
    dkc = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'need'


class NeedFamily(models.Model):
    id_family = models.ForeignKey(Family, models.DO_NOTHING, db_column='id_family', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    id_need = models.ForeignKey(Need, models.DO_NOTHING, db_column='id_need')
    created = models.DateTimeField()
    updated = models.DateTimeField()
    user_avatar = models.TextField(blank=True, null=True)
    user_role = models.IntegerField(blank=True, null=True)
    username = models.TextField()
    type = models.TextField()
    address = models.ForeignKey(NakamaOwners, models.DO_NOTHING, db_column='address', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'need_family'


class NeedReceipt(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    need = models.ForeignKey(Need, models.DO_NOTHING)
    sw = models.ForeignKey('SocialWorker', models.DO_NOTHING)
    receipt = models.ForeignKey('Receipt', models.DO_NOTHING)
    deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'need_receipt'
        unique_together = (('need', 'receipt', 'deleted'),)


class Ngo(models.Model):
    coordinatorid = models.ForeignKey('SocialWorker', models.DO_NOTHING, db_column='coordinatorId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=1000)
    postaladdress = models.TextField(db_column='postalAddress')  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress', max_length=1000)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=1000)  # Field name made lowercase.
    logourl = models.CharField(db_column='logoUrl', max_length=1000)  # Field name made lowercase.
    balance = models.IntegerField()
    socialworkercount = models.IntegerField(db_column='socialWorkerCount')  # Field name made lowercase.
    childrencount = models.IntegerField(db_column='childrenCount')  # Field name made lowercase.
    registerdate = models.DateTimeField(db_column='registerDate')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    city = models.IntegerField()
    country = models.IntegerField()
    currentsocialworkercount = models.IntegerField(db_column='currentSocialWorkerCount')  # Field name made lowercase.
    currentchildrencount = models.IntegerField(db_column='currentChildrenCount')  # Field name made lowercase.
    website = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ngo'


class Payment(models.Model):
    id_need = models.ForeignKey(Need, models.DO_NOTHING, db_column='id_need', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    gateway_payment_id = models.CharField(max_length=1000, blank=True, null=True)
    order_id = models.CharField(unique=True, max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    need_amount = models.IntegerField(blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    card_no = models.CharField(max_length=1000, blank=True, null=True)
    hashed_card_no = models.CharField(max_length=1000, blank=True, null=True)
    gateway_track_id = models.CharField(max_length=1000, blank=True, null=True)
    donation_amount = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    credit_amount = models.IntegerField(blank=True, null=True)
    use_credit = models.BooleanField()
    verified = models.DateTimeField(blank=True, null=True)
    is_nakama = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'payment'


class Receipt(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    owner = models.ForeignKey('SocialWorker', models.DO_NOTHING)
    attachment = models.CharField(max_length=128)
    code = models.CharField(max_length=64)
    deleted = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    is_public = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receipt'
        unique_together = (('code', 'deleted'),)


class ResetPassword(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    token = models.CharField(unique=True, max_length=1000)
    expire_at = models.DateTimeField()
    is_used = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reset_password'


class SocialWorker(models.Model):
    generatedcode = models.CharField(db_column='generatedCode', max_length=1000)  # Field name made lowercase.
    id_ngo = models.ForeignKey(Ngo, models.DO_NOTHING, db_column='id_ngo')
    id_type = models.ForeignKey('SocialWorkerType', models.DO_NOTHING, db_column='id_type')
    firstname = models.CharField(db_column='firstName', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=1000)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=1000)  # Field name made lowercase.
    password = models.CharField(max_length=1000)
    birthcertificatenumber = models.CharField(db_column='birthCertificateNumber', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    idnumber = models.CharField(db_column='idNumber', max_length=1000)  # Field name made lowercase.
    idcardurl = models.CharField(db_column='idCardUrl', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    passportnumber = models.CharField(db_column='passportNumber', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    birthdate = models.DateField(db_column='birthDate', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=1000)  # Field name made lowercase.
    emergencyphonenumber = models.CharField(db_column='emergencyPhoneNumber', max_length=1000)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress', max_length=1000)  # Field name made lowercase.
    telegramid = models.CharField(db_column='telegramId', max_length=1000)  # Field name made lowercase.
    postaladdress = models.TextField(db_column='postalAddress', blank=True, null=True)  # Field name made lowercase.
    avatarurl = models.CharField(db_column='avatarUrl', max_length=1000)  # Field name made lowercase.
    childcount = models.IntegerField(db_column='childCount')  # Field name made lowercase.
    needcount = models.IntegerField(db_column='needCount')  # Field name made lowercase.
    bankaccountnumber = models.CharField(db_column='bankAccountNumber', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    bankaccountshebanumber = models.CharField(db_column='bankAccountShebaNumber', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    bankaccountcardnumber = models.CharField(db_column='bankAccountCardNumber', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    registerdate = models.DateField(db_column='registerDate')  # Field name made lowercase.
    lastlogindate = models.DateField(db_column='lastLoginDate')  # Field name made lowercase.
    lastlogoutdate = models.DateField(db_column='lastLogoutDate', blank=True, null=True)  # Field name made lowercase.
    passporturl = models.CharField(db_column='passportUrl', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    gender = models.BooleanField()
    city = models.IntegerField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    currentchildcount = models.IntegerField(db_column='currentChildCount')  # Field name made lowercase.
    currentneedcount = models.IntegerField(db_column='currentNeedCount')  # Field name made lowercase.
    locale = models.CharField(max_length=10)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_worker'


class SocialWorkerType(models.Model):
    name = models.CharField(max_length=1000)
    privilege = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_worker_type'


class User(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=1000)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=1000)  # Field name made lowercase.
    avatarurl = models.CharField(db_column='avatarUrl', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', unique=True, max_length=1000)  # Field name made lowercase.
    birthdate = models.DateField(db_column='birthDate', blank=True, null=True)  # Field name made lowercase.
    birthplace = models.CharField(db_column='birthPlace', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    flagurl = models.CharField(db_column='flagUrl', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress', unique=True, max_length=1000, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=10, blank=True, null=True)
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    city = models.IntegerField()
    lastlogin = models.DateTimeField(db_column='lastLogin')  # Field name made lowercase.
    field_password = models.CharField(db_column='_password', max_length=1000)  # Field renamed because it started with '_'.
    locale = models.CharField(max_length=10)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    country = models.CharField(max_length=8, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    is_email_verified = models.BooleanField()
    is_phonenumber_verified = models.BooleanField()
    postal_address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    is_installed = models.BooleanField()
    is_nakama = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'user'


class UserFamily(models.Model):
    id_family = models.ForeignKey(Family, models.DO_NOTHING, db_column='id_family')
    userrole = models.IntegerField(db_column='userRole')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_user')
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_family'


class Verification(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    field_code = models.CharField(db_column='_code', max_length=6)  # Field renamed because it started with '_'.
    expire_at = models.DateTimeField()
    type = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'verification'
