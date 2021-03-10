# Library's
import os
import json

# Import src files
import src.exceptions as exception


class languageHelper:
    def __init__(self):
        self.environment = os.environ["PYTHONPATH"].split(os.pathsep)[0]
        self.__lang_path = self.environment + "/app/languages/"
        self.__lang_exceptions = []
        self.__default_language = self.__lang_path + "english.json"
        self.__config = self.__lang_path + "config/config.json"
        self.__found_languages_files = self.__getAllLanguageFiles()
        self.found_languages = self.__getAllLanguages()

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

    def __getLastLanguage(self) -> dict:
        with open(self.__config, "r") as file:
            last_lang = json.load(file)
        return last_lang

    def __setLastLanguage(self, language_dict: dict) -> bool:
        with open(self.__config, "w") as file:
            json.dump(language_dict, file)
        return True

    def getLanguage(self, language: str = None) -> dict:
        if language is None:
            language = self.__getLastLanguage()["last_lang"]

        if language not in self.__found_languages_files:
            if language not in self.found_languages:
                raise exception.LanguageNotFound(language)
            index = self.found_languages.index(language)
            language = self.__found_languages_files[index]

        language_json = self.__getLastLanguage()
        language_json["last_lang"] = language
        self.__setLastLanguage(language_json)

        with open(self.__lang_path + language, "r") as lang:
            return json.load(lang)


