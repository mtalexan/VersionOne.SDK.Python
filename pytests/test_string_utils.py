from v1pysdk.string_utils import split_attribute

import pytest

class TestStringUtils():

    def test_split_attribute(self):
        assert((['[testing]]'] == split_attribute('[testing]]')))
        assert(['[[testing]'] == split_attribute('[[testing]'))
        assert(['testing','a','sentence','is','difficult'] == split_attribute('testing.a.sentence.is.difficult'))
        assert(['testing','[a.sentence]','is','difficult'] == split_attribute('testing.[a.sentence].is.difficult'))
        assert(['testing[.a.sentence]','is', 'difficult'] == split_attribute('testing[.a.sentence].is.difficult'))
        assert(['testing','a[.sentence.]is','difficult'] == split_attribute('testing.a[.sentence.]is.difficult'))
        assert(['testing','a','sentence','is','difficult]'] == split_attribute('testing.a.sentence.is.difficult]'))
        assert(['testing', 'a','sentence','is',']difficult'] == split_attribute('testing.a.sentence.is.]difficult'))
        assert(['[testing.a.sentence.is]','difficult'] == split_attribute('[testing.a.sentence.is].difficult'))
        assert(['[testing.][a.sentence.is.difficult]'] == split_attribute('[testing.][a.sentence.is.difficult]'))
        assert(['[testing]','[a]','[sentence]','[is]','[difficult]'] ==
                          split_attribute('[testing].[a].[sentence].[is].[difficult]'))
        assert(['testing','[[a.sentence.]is]','difficult'] ==
                          split_attribute('testing.[[a.sentence.]is].difficult'))
        assert(["History[Status.Name='Done']"] == split_attribute("History[Status.Name='Done']"))
        assert(["ParentMeAndUp[Scope.Workitems.@Count='2']"] ==
                          split_attribute("ParentMeAndUp[Scope.Workitems.@Count='2']") )
        assert(["Owners","OwnedWorkitems[ChildrenMeAndDown=$]","@DistinctCount"] ==
                          split_attribute("Owners.OwnedWorkitems[ChildrenMeAndDown=$].@DistinctCount") )
        assert(["Workitems[ParentAndUp[Scope=$].@Count='1']"] ==
                          split_attribute("Workitems[ParentAndUp[Scope=$].@Count='1']") )
        assert(["RegressionPlan","RegressionSuites[AssetState!='Dead']","TestSets[AssetState!='Dead']","Environment", "@DistinctCount"]
                           == split_attribute("RegressionPlan.RegressionSuites[AssetState!='Dead'].TestSets[AssetState!='Dead'].Environment.@DistinctCount") )
        assert(["Scope","ChildrenMeAndDown","Workitems:Story[ChildrenMeAndDown.ToDo.@Sum!='0.0']","Estimate","@Sum"]
                          == split_attribute("Scope.ChildrenMeAndDown.Workitems:Story[ChildrenMeAndDown.ToDo.@Sum!='0.0'].Estimate.@Sum") )
