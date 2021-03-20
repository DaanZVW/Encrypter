# Library's
import os
import json
import googletrans
from typing import Union, Any

# Import src files
import app.lib.utils as utils
import src.exceptions as exception

# Import GUI files
import app.lib.popup as popup


class languageHelper:
    def __init__(self):
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
            self.__openFile(self.__config_path, "r")
        except FileNotFoundError:
            self.__openFile(self.__config_path, "w", lambda file: file.write("{\n}"))


    def __openFile(self, filename: str, mode: str, function = None):
        """
        Returns the function with filestream of filename
        :param filename: Name of the file
        :param mode: Mode which the file will be opened with
        :param function: Function on filestream
        :return: Result of function with filestream
        """
        with open(filename, mode) as file:
            if function is not None:
                return function(file)

    def __getAllLanguageFiles(self):
        all_files = list(filter(lambda file: os.path.isfile(f"{self.__lang_path}{file}"), os.listdir(self.__lang_path)))
        all_files = list(filter(lambda file: file not in self.__lang_exceptions, all_files))
        return all_files

    def __getAllLanguages(self):
        languages = []
        for language in self.__getAllLanguageFiles():
            self.__openFile(self.__lang_path + language, "r",
                            lambda file: languages.append(json.load(file)["language"]))
        return languages

    def __getConfig(self) -> dict:
        return self.__openFile(self.__config_path, "r", json.load)

    def __setConfig(self, language_dict: dict) -> bool:
        return self.__openFile(self.__config_path, "w", lambda file: json.dump(language_dict, file,
                                                                               indent=self.__indent_json))

    def __languageApiExist(self, language: str) -> Union[tuple[bool, Any], tuple[bool, None]]:
        for short_lang, full_lang in googletrans.LANGUAGES.items():
            if language in [short_lang, full_lang]:
                return True, short_lang
        return False, None

    def __doOnValuesFromDict(self, curr_dict: dict, function) -> dict:
        new_dict = {}
        for key in curr_dict.keys():
            if type(curr_dict[key]) is dict:
                new_dict[key] = self.__doOnValuesFromDict(curr_dict[key], function)
            else:
                new_dict[key] = function(curr_dict[key])
        return new_dict

    def __getAmountValues(self, curr_dict: dict) -> int:
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
        def __getValues(translate_language):
            """
            Callback function for setting new_lang variable
            :param translate_language:
            """
            global new_lang
            new_lang = translate_language

        global new_lang
        new_lang = {}

        lang_data = self.__openFile(self.__default_language_path, "r", json.load)
        lang_data["language"] = googletrans.LANGUAGES[language]

        translator = googletrans.Translator()
        popup_window = popup.progressbarStep(
            popup.progressbarSetting.showReturn,
            self.__getAmountValues(lang_data),
            utils.langCall(lang_data, "button", "translate", "popup_text"),
        )

        try:
            popup_window.setFunctions(
                lambda: self.__doOnValuesFromDict(
                    lang_data,
                    utils.multiFunc(
                        lambda value: translator.translate(value, src="en", dest=language).text,
                        lambda value: popup_window.step(1),
                        lambda value: popup_window.update_idletasks()
                    )
                ),
                __getValues
            )
            popup_window.mainloop()

        except AttributeError:
            raise exception.TranslatingFailedLibrary

        if self.__getAmountValues(new_lang) <= 0:
            raise exception.TranslatingFailed

        lang_file_name = googletrans.LANGUAGES[language] + ".json"
        self.__openFile(self.__lang_path + lang_file_name, "w",
                        lambda file: json.dump(new_lang, file, indent=self.__indent_json))
        return lang_file_name

    def getLanguage(self, language: str = None) -> dict:
        if language is None:
            try:
                language = self.__getConfig()["last_lang"]
            except KeyError:
                language = self.__default_language

        if language not in self.__found_languages_files:
            if language in self.found_languages:
                index = self.found_languages.index(language)
                language = self.__found_languages_files[index]

            elif (lang_info := self.__languageApiExist(language))[0]:
                language = self.__makeNewLanguage(lang_info[1])
                self.__found_languages_files = self.__getAllLanguageFiles()

            else:
                raise exception.LanguageNotFound(language)

        language_json = self.__getConfig()
        language_json["last_lang"] = language
        self.__setConfig(language_json)

        return self.__openFile(self.__lang_path + language, "r", lambda file: json.load(file))
