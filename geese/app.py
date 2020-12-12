import datetime
from collections import Counter
from functools import lru_cache as _lru_cache
from typing import List as _List
from typing import Type as _Type
from typing import TypeVar as _TypeVar
from typing import Any as _Any
from typing import Tuple as _Tuple
from typing import Iterable as _Iterable

C = _TypeVar('C')

class Processor:
    app = None
    def process(self, *args, **kwagrs):
        raise NotImplementedError

class App:
    def __init__(self):
        self._processors = []
        self._setup_processors = []
        self._next_entity_id = 0
        self._components = {}
        self._entities = {}
        self._dead_entities= set()
        self._last_delta = 0.0


    def add_processor(self, processor_instance: Processor, priority=0) -> None:
        assert issubclass(processor_instance.__class__, Processor)

        processor_instance.world = self
        processor_instance.priority = priority

        self._processors.append(processor_instance)
        self._processors.sort(key = lambda proc: proc.priority, reverse=True)
        return self


    def add_setup_processor(self, processor_instance: Processor) -> None:
        assert issubclass(processor_instance.__class__, Processor)

        processor_instance.world = self
        self._setup_processors.append(processor_instance)


    def get_components(
            self, 
            *component_types: _Type
    ) -> _Iterable[_Tuple[int, ...]]:
        return self._get_components(*component_types).items()

    def _get_components(self, *component_types: _Type) -> _Iterable[_Tuple[int, ...]]:
        ents = self._entities
        comps = self._components

        match_comps = {}
        for key, val in comps.items():
            if [*component_types] == [type(t) for t in val]: 
                match_comps[key] = val

        return match_comps


    def _get_component():
        pass


    def _process(self, *args, **kwargs):
        for processor in self._processors:
            processor.process(*args, **kwargs)

    
    def _process_setup(self, *args, **kwargs):
        for processor in self._setup_processors:
            processor.process(*args, **kwargs)


    def loop_process(self, *args, **kwargs):
        self._process_setup(*args, **kwargs) 
        while True:
            start = datetime.datetime.now()
            self._process(*args, **kwargs)
            self._last_delta = (datetime.datetime.now() - start).total_seconds() * 1000 
