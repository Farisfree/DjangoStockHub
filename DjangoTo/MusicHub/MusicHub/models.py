# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Searchresult(models.Model):
    searchinformation = models.CharField(db_column='searchInformation', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'searchresult'


class SongData(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    title = models.CharField(max_length=250)
    artist = models.CharField(max_length=190)
    album = models.CharField(max_length=190)
    times = models.CharField(max_length=50)
    search_time = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'song_data'


class UsersTable(models.Model):
    id = models.CharField(max_length=20, null=False, primary_key=True)
    password1 = models.CharField(db_column='Password1', max_length=20)  # Field name made lowercase.
    usertype = models.IntegerField(db_column='UserType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'users_table'
