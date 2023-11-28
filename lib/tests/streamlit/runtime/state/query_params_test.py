# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from streamlit.errors import StreamlitAPIException
from streamlit.runtime.state.query_params import QueryParams
from tests.delta_generator_test_case import DeltaGeneratorTestCase


class QueryParamsMethodTests(DeltaGeneratorTestCase):
    def setUp(self):
        super().setUp()
        self.query_params = QueryParams()
        self.query_params._query_params = {"foo": "bar", "two": ["x", "y"]}

    def test__getitem__raises_KeyError_for_nonexistent_key(self):
        with pytest.raises(KeyError):
            self.query_params["nonexistent"]

    def test__getitem__returns_last_element_of_list(self):
        assert self.query_params["two"] == "y"

    def test__getitem__retrieves_existing_key(self):
        assert self.query_params["foo"] == "bar"

    def test__setitem__converts_int_value_to_string(self):
        self.query_params["baz"] = 1
        assert self.query_params["baz"] == "1"
        message = self.get_message_from_queue(0)
        assert "baz=1" in message.page_info_changed.query_string

    def test__setitem__converts_float_value_to_string(self):
        self.query_params["corge"] = 1.23
        assert self.query_params["corge"] == "1.23"
        message = self.get_message_from_queue(0)
        assert "corge=1.23" in message.page_info_changed.query_string

    def test__setitem__adds_new_str_query_param(self):
        assert "test" not in self.query_params
        self.query_params["test"] = "test"
        assert self.query_params.get("test") == "test"
        message = self.get_message_from_queue(0)
        assert "test=test" in message.page_info_changed.query_string

    def test__setitem__adds_empty_string_value(self):
        assert "test" not in self.query_params
        self.query_params["test"] = ""
        assert self.query_params["test"] == ""
        message = self.get_message_from_queue(0)
        assert "test=" in message.page_info_changed.query_string

    def test__setitem__adds_list_value(self):
        self.query_params["test"] = ["test", "test2"]
        assert self.query_params["test"] == "test2"
        message = self.get_message_from_queue(0)
        assert "test=test&test=test2" in message.page_info_changed.query_string

    def test__setitem__sets_old_query_param_key(self):
        self.query_params["foo"] = "test"
        assert self.query_params.get("foo") == "test"
        message = self.get_message_from_queue(0)
        assert "foo=test" in message.page_info_changed.query_string

    def test__delitem__removes_existing_key(self):
        del self.query_params["foo"]
        assert "foo" not in self.query_params
        message = self.get_message_from_queue(0)
        assert "two=x&two=y" in message.page_info_changed.query_string
        assert "foo" not in message.page_info_changed.query_string

    def test__delitem__raises_error_for_nonexistent_key(self):
        with pytest.raises(KeyError):
            del self.query_params["nonexistent"]

    def test_get_all_returns_empty_list_for_nonexistent_key(self):
        assert self.query_params.get_all("nonexistent") == []

    def test_get_all_retrieves_single_element_list(self):
        assert self.query_params.get_all("foo") == ["bar"]

    def test_get_all_retrieves_multiple_values_as_list(self):
        assert self.query_params.get_all("two") == ["x", "y"]

    def test_get_all_handles_mixed_type_values(self):
        self.query_params["test"] = ["", "a", 1, 1.23]
        assert self.query_params.get_all("test") == ["", "a", "1", "1.23"]

    def test_clear_removes_all_query_params(self):
        self.query_params.clear()
        assert len(self.query_params) == 0
        message = self.get_message_from_queue(0)
        assert "" in message.page_info_changed.query_string

    def test__setitem__raises_exception_for_embed_key(self):
        with pytest.raises(StreamlitAPIException):
            self.query_params["embed"] = True

    def test__setitem__raises_exception_for_embed_options_key(self):
        with pytest.raises(StreamlitAPIException):
            self.query_params["embed_options"] = "show_toolbar"

    def test_to_dict(self):
        self.query_params["baz"] = ""
        result_dict = {"foo": "bar", "two": "y", "baz": ""}
        assert self.query_params.to_dict() == result_dict
