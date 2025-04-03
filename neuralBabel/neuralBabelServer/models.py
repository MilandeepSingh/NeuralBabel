from django.db import models

class Language(models.Model):
    language_name = models.CharField(max_length=100, primary_key=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.language_name

class Word(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    english_translation = models.CharField(max_length=100)
    english_transliteration = models.CharField(max_length=100)

    class Meta:
        unique_together = ('language', 'word')

    def __str__(self):
        return self.word

class User(models.Model):
    email_id = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
    languages = models.ManyToManyField(Language)
    words_learnt = models.ManyToManyField(Word)

    def __str__(self):
        return self.name