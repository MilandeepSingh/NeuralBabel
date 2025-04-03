from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
from .models import User, Language, Word

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.db import IntegrityError

def fetch_profile(request):
    # Hardcoded user email
    hardcoded_email = 'user@example.com'
    
    # Retrieve the user by the hardcoded email
    user = get_object_or_404(User, email_id=hardcoded_email)

    # Initialize a dictionary to hold the language and word count
    language_word_count = {}

    # Iterate over each language learned by the user
    for language in user.languages.all():
        # Count the number of words learned for each language
        word_count = user.words_learnt.filter(language=language).count()
        language_word_count[language.language_name] = word_count

    # Return the dictionary as JSON response
    return JsonResponse(language_word_count)

def fetch_words_for_language(request, language_name):
    # Hardcoded user email
    hardcoded_email = 'user@example.com'
    
    # Retrieve the user by the hardcoded email
    user = get_object_or_404(User, email_id=hardcoded_email)

    # Retrieve the language object based on the given language name
    language = get_object_or_404(Language, language_name=language_name)

    # Initialize a list to hold the word details
    words_details = []

    # Iterate over each word learned by the user in the specified language
    for word in user.words_learnt.filter(language=language):
        words_details.append({
            'word': word.word,
            'english_translation': word.english_translation,
            'english_transliteration': word.english_transliteration,
        })

    # Return the list of word details as JSON response
    return JsonResponse({'words': words_details})

def add_existing_language_to_user(request, language_name):
    # Hardcoded user email
    hardcoded_email = 'user@example.com'
    
    # Retrieve the user by the hardcoded email
    user = get_object_or_404(User, email_id=hardcoded_email)

    # Retrieve the existing language object
    language = get_object_or_404(Language, language_name=language_name)

    # Add the language to the user's learned languages
    user.languages.add(language)

    return JsonResponse({'status': 'success', 'message': f'Language {language_name} associated with user.'})

def add_new_word(language_name, word, english_translation, english_transliteration):
    # Retrieve the language object based on the given language name
    language = get_object_or_404(Language, language_name=language_name)

    try:
        # Create a new Word object
        new_word = Word.objects.create(
            language=language,
            word=word,
            english_translation=english_translation,
            english_transliteration=english_transliteration
        )
        return JsonResponse({'status': 'success', 'message': f'New word {word} added to language {language_name}.'})
    except IntegrityError:
        return JsonResponse({'status': 'error', 'message': f'Failed to add the word due to a database integrity issue.'})

# Replace it with api to llm to get translation and transliteration of the word
def dummy_translation_function(word, language):
    # Dummy function to provide translation and transliteration
    # This should be replaced with actual logic or API calls
    return {
        'english_translation': f'Translation of {word}',
        'english_transliteration': f'Transliteration of {word}'
    }

def associate_word_with_user(request, language_name, word):
    # Hardcoded user email
    hardcoded_email = 'user@example.com'
    
    # Retrieve the user by the hardcoded email
    user = get_object_or_404(User, email_id=hardcoded_email)

    # Retrieve the language object based on the given language name
    language = get_object_or_404(Language, language_name=language_name)

    # Check if the word exists for the given language
    existing_word = Word.objects.filter(language=language, word=word).first()

    if existing_word:
        # Check if the word is already associated with the user
        if user.words_learnt.filter(id=existing_word.id).exists():
            return JsonResponse({'status': 'ignored', 'message': f'Word {word} already learned by the user.'})
        else:
            user.words_learnt.add(existing_word)
            return JsonResponse({'status': 'success', 'message': f'Word {word} associated with user.'})
    else:
        # Call dummy function to get translation and transliteration
        word_details = dummy_translation_function(word, language)

        # Call the add_new_word method to add the word to the language
        add_new_word(language_name, word, word_details['english_translation'], word_details['english_transliteration'])

        # Retrieve the newly added word and associate it with the user
        new_word = Word.objects.get(language=language, word=word)
        user.words_learnt.add(new_word)

        return JsonResponse({'status': 'success', 'message': f'New word {word} learned and associated with user.'})