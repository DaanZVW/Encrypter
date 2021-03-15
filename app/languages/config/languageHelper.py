# Library's
import os
import json

# Import src files
import src.exceptions as exception
import googletrans


class languageHelper:
    def __init__(self):
        self.environment = os.environ["PYTHONPATH"].split(os.pathsep)[0]
        self.__lang_path = self.environment + "/app/languages/"
        self.__lang_exceptions = []
        self.__default_language = self.__lang_path + "english.json"
        self.__config = self.__lang_path + "config/config.json"
        self.__found_languages_files = self.__getAllLanguageFiles()
        self.__indent_json = 4
        self.found_languages = self.__getAllLanguages()

    def __openFile(self, filename: str, mode: str, function):
        with open(filename, mode) as file:
            return function(file)

    def __getAllLanguageFiles(self):
        all_files = list(filter(lambda file: os.path.isfile(f"{self.__lang_path}{file}"), os.listdir(self.__lang_path)))
        all_files = list(filter(lambda file: file not in self.__lang_exceptions, all_files))
        return all_files

    def __getAllLanguages(self):
        languages = []
        for language in self.__getAllLanguageFiles():
            with open(f"{self.__lang_path}{language}", "r") as file:
                languages.append(json.load(file)["language"])
        return languages

    def __getConfig(self) -> dict:
        return self.__openFile(self.__config, "r", json.load)

    def __setConfig(self, language_dict: dict) -> bool:
        return self.__openFile(self.__config, "w", lambda file: json.dump(language_dict, file,
                                                                          indent=self.__indent_json))

    def __languageApiExist(self, language: str) -> bool:
        for short_lang, full_lang in googletrans.LANGUAGES.items():
            if language in [short_lang, full_lang]:
                return True
        return False

    def __doOnValuesFromDict(self, curr_dict: dict, function) -> dict:
        new_dict = {}
        for key in curr_dict.keys():
            if type(curr_dict[key]) is dict:
                new_dict[key] = self.__doOnValuesFromDict(curr_dict[key], function)
            else:
                new_dict[key] = function(curr_dict[key])
        return new_dict

    def __makeNewLanguage(self, language: str) -> dict:
        lang_data = self.__openFile(self.__default_language, "r", json.load)
        translator = googletrans.Translator()
        new_lang = self.__doOnValuesFromDict(
            lang_data, lambda value: translator.translate(value, src="en", dest=language).text)

        lang_file_name = googletrans.LANGUAGES[language] + ".json"
        self.__openFile(self.__lang_path + lang_file_name, "w",
                        lambda file: json.dump(new_lang, file, indent=self.__indent_json))
        return lang_file_name

    def getLanguage(self, language: str = None) -> dict:
        if language is None:
            language = self.__getConfig()["last_lang"]

        if language not in self.__found_languages_files:
            if language in self.found_languages:
                index = self.found_languages.index(language)
                language = self.__found_languages_files[index]

            elif self.__languageApiExist(language):
                language = self.__makeNewLanguage(language)
                self.__found_languages_files = self.__getAllLanguageFiles()

            else:
                raise exception.LanguageNotFound(language)

        language_json = self.__getConfig()
        language_json["last_lang"] = language
        self.__setConfig(language_json)

        return self.__openFile(self.__lang_path + language, "r", lambda file: json.load(file))



