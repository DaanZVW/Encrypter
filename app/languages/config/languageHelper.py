# Library's
import os
import json
import googletrans
from typing import Union, Any

# Import src files
import app.lib.utils as utils
import src.exceptions as exception
from app.lib.utils import openFile

# Import GUI files
import app.lib.popup as popup


class languageHelper:
    """
    Helps with interacting with languages
    """

    def __init__(self):
        """
        Constructor for the languagehelper class
        """
        self.environment = os.environ["PYTHONPATH"].split(os.pathsep)[0]
        self.__lang_path = self.environment + "/app/languages/"
        self.__lang_exceptions = []
        self.__default_language = "english.json"
        self.__default_language_path = self.__lang_path + self.__default_language
        self.__config_path = self.__lang_path + "config/config.json"
        self.__found_languages_files = self.__getAllLanguageFiles()
        self.__indent_json = 4
        self.found_languages = self.__getAllLanguages()

        try:
            openFile(self.__config_path, "r")
        except FileNotFoundError:
            openFile(self.__config_path, "w", lambda file: file.write("{\n}"))

    def __getAllLanguageFiles(self):
        """
        Gets all the language files available to the encrypter
        :return: List with all language file names
        """
        all_files = list(filter(lambda file: os.path.isfile(f"{self.__lang_path}{file}"), os.listdir(self.__lang_path)))
        all_files = list(filter(lambda file: file not in self.__lang_exceptions, all_files))
        return all_files

    def __getAllLanguages(self):
        """
        Gets all the internal language names of all language files available to the encrypter
        :return: List with language names in the language files
        """
        languages = []
        for language in self.__getAllLanguageFiles():
            openFile(self.__lang_path + language, "r",
                     lambda file: languages.append(json.load(file)["language"]))
        return languages

    def __languageApiExist(self, language: str) -> Union[tuple[bool, str], tuple[bool, None]]:
        """
        Returns if given language is available in the googletrans library
        :param language: Language that needs checking
        :return: Boolean, key of the given language
        """
        for short_lang, full_lang in googletrans.LANGUAGES.items():
            if language in [short_lang, full_lang]:
                return True, short_lang
        return False, None

    def __doOnValuesFromDict(self, curr_dict: dict, function: Any) -> dict:
        """
        Function that does function recursively on given dict
        :param curr_dict: Dictionary that is getting checked
        :param function: Function which each element is run over
        :return: Dictionary with changes of function
        """
        new_dict = {}
        for key in curr_dict.keys():
            if type(curr_dict[key]) is dict:
                new_dict[key] = self.__doOnValuesFromDict(curr_dict[key], function)
            else:
                new_dict[key] = function(curr_dict[key])
        return new_dict

    def __getAmountValues(self, curr_dict: dict) -> int:
        """
        Get the amount
        :param curr_dict:
        :return:
        """
        amount = 0
        for key in curr_dict.keys():
            if type(curr_dict[key]) is dict:
                amount += self.__getAmountValues(curr_dict[key])
            else:
                amount += 1
        return amount

    def __makeNewLanguage(self, language: str) -> dict:
        """
        Generate a new language using the googletrans library
        :param language: Language that needs translating
        :return: Translated dict with language format
        """
        try:
            last_lang = openFile(self.__config_path, "r", json.load)["last_lang"]
            old_lang_data = openFile(self.__lang_path + last_lang,
                                     "r", lambda file: json.load(file))
        except FileNotFoundError:
            old_lang_data = openFile(self.__lang_path + self.__default_language,
                                     "r", lambda file: json.load(file))

        default_lang_data = openFile(self.__default_language_path, "r", json.load)
        default_lang_data["language"] = googletrans.LANGUAGES[language]

        new_lang = {}
        translator = googletrans.Translator()

        popup_window = popup.progressbarStep(
            utils.langCall(old_lang_data, "button", "translate", "title"),
            utils.langCall(old_lang_data, "button", "translate", "popup_text"),
            self.__getAmountValues(default_lang_data),
            utils.multiFunc(lambda translated_lang: new_lang.update(translated_lang)),
            utils.multiFunc(lambda value: translator.translate(value, src="en", dest=language).text)
        )
        popup_window.function = utils.callbackFunc(self.__doOnValuesFromDict, default_lang_data, popup_window.function)

        try:
            popup_window.mainloop()

        except AttributeError:
            raise exception.TranslatingFailedLibrary

        if self.__getAmountValues(new_lang) <= 0:
            raise exception.TranslatingFailed

        lang_file_name = googletrans.LANGUAGES[language] + ".json"
        openFile(self.__lang_path + lang_file_name, "w",
                 lambda file: json.dump(new_lang, file, indent=self.__indent_json))
        return lang_file_name

    def getLanguage(self, language: str = None) -> dict:
        if language is None:
            try:
                language = openFile(self.__config_path, "r", json.load)["last_lang"]
            except KeyError:
                language = self.__default_language

            if not os.path.exists(self.__lang_path + language):
                language = self.__default_language

        if language not in self.__found_languages_files:
            if language in self.found_languages:
                index = self.found_languages.index(language)
                language = self.__found_languages_files[index]

            elif self.__languageApiExist(language):
                language = self.__makeNewLanguage(language)
                self.__found_languages_files = self.__getAllLanguageFiles()
                self.found_languages = self.__getAllLanguages()

            else:
                raise exception.LanguageNotFound(language)

        language_json = openFile(self.__config_path, "r", json.load)
        language_json["last_lang"] = language
        openFile(self.__config_path, "w", lambda file: json.dump(language_json, file,
                                                                 indent=self.__indent_json))

        try:
            return openFile(self.__lang_path + language, "r", lambda file: json.load(file))
        except FileNotFoundError:
            raise exception.LanguageNotFound(language)
