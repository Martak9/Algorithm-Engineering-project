from StdGraphGenerator import StdGraphGenerator
import json

class GraphGeneratorFactory:

    _config_file: str
    _configuration: str

    def __new__(cls, config_file="./generator_config.json"):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GraphGeneratorFactory, cls).__new__(cls)
            cls.instance._config_file = config_file
            with open(config_file, 'r') as file:
                cls.instance._configuration = json.load(file)
        return cls.instance

    def reload_config(self):
        with open(self._config_file, 'r') as file:
            self._configuration = json.load(file)

    def get_generator(self):
        generator_class_name = self._configuration['generator']
        generator_class = globals()[generator_class_name]
        params = self._configuration[generator_class_name]
        return generator_class(**params)

if __name__ == '__main__':
    generator = GraphGeneratorFactory().get_generator()
    generator.run()


