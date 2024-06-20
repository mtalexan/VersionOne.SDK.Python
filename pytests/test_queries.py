import v1pysdk
import common_test_server
import test_common_setup
import pytest

class TestV1Query(test_common_setup.TestV1CommonSetup):
    def test_select_story_as_generic_asset(self):
        """Queries up to 5 story assets"""
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.AssetType.select('Name').where(Name='Story').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Story on the test server
            assert(querySucceeded == True)
            assert((0 < size < 6) == True)

    def test_select_story(self):
        """Queries up to 5 stories"""
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Story.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Story on the test server
            assert(querySucceeded == True)
            assert((0 < size < 6) == True)

    def test_select_epic(self):
        """Queries up to 5 Epics, called Portfolios in the GUI.
           In order to create a new Story, we must be able to query for an Epic we want to put it under,
           and pass that returned Epic object as the Super of the new Story.  This confirms the Epic query
           part always works.
        """
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Epic.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Portfolio Item on the test server
            assert(querySucceeded == True)
            assert((0 < size < 6) == True)


    def test_select_scope(self):
        """Queries up to 5 Scopes, called Projects in the GUI.
           In order to create a new Story, we must be able to query for a Scope we want to put it under,
           and pass that returned Scope object as the Scope of the new Story.  This confirms the Scope query
           part always works.
        """
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Scope.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Project on the test server
            assert(querySucceeded == True)
            assert((0 < size < 6) == True)

    def test_select_task(self):
        """Queries up to 5 Tasks.
        """
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Task.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Task on the test server
            assert(querySucceeded == True)
            assert((0 < size < 6) == True)

    def test_non_default_query(self):
        """Queries an attribute that's not retrieved by default from a Story so it will requery for the specific
           attribute that was requested.
        """
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            failedFetchCreateDate = False
            failedFetchName = False
            s = v1.Story.select('Name').page(size=1)
            try:
                junk = s.CreateDate # fetched on demand, not default
            except:
                failedFetchCreateDate = True

            assert(failedFetchCreateDate == False)

            try:
                junk = s.Name # fetched by default on initial query
            except:
                failedFetchName = True

            assert(failedFetchName == False)


    def test_sum_query(self):
        """Queries for a summation of values of a numeric field (Actuals.Value) across a set of assests (Tasks).
        """
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            foundActuals=False
            exceptionReached=False
            try:
                tasks = v1.Task.select('Name','Actuals.Value.@Sum').page(size=30)
                tasks.first() #perform the actual query
                if len(tasks) <= 0:
                    pytest.skip("Test server contains no Tasks")
                    return
                else:
                    for t in tasks:
                        if 'Actuals.Value.@Sum' in t.data:
                            foundActuals=True
                            break
            except:
                exceptionReached=True
            else:
                if not foundActuals:
                    pytest.skip("Test server Tasks contained no Actuals.Value's")
                    return

            assert(exceptionReached == False)

    def test_find_query(self):
        """Creates a story, then does a find to see if it can be located by a partial name from a separate
           connection instance.
        """
        searchName=""
        exceptionReached=False
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1create:
            createdStory = self.test_initial_create_story(v1create)

            # make a search term that's just one character shorter
            searchName = createdStory.Name[:-1]

        with common_test_server.PublicTestServerConnection.getV1Meta() as v1find:
            findItems = None
            findItem = None
            size = 0
            firstName = ""
            try:
                findItems = v1find.Story.select('Name').find(text=searchName, field='Name')
                findItem = findItems.first() #actually run the query
                size = len(findItems)
                firstName = findItem.Name
            except Exception as e:
                raise e
                #exceptions here are almost always because the query failed to work right
                exceptionReached=True
            else:
                # at the very least we should have found the one we based the search string on
                assert(size > 0)
                # results need to contain the string we searched for
                assert((searchName in firstName) == True)

            assert(exceptionReached == False)

