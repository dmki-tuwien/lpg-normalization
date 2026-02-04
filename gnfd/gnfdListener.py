# Generated from gnfd.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gnfdParser import gnfdParser
else:
    from gnfdParser import gnfdParser

# This class defines a complete listener for a parse tree produced by gnfdParser.
class gnfdListener(ParseTreeListener):

    # Enter a parse tree produced by gnfdParser#dependency.
    def enterDependency(self, ctx:gnfdParser.DependencyContext):
        pass

    # Exit a parse tree produced by gnfdParser#dependency.
    def exitDependency(self, ctx:gnfdParser.DependencyContext):
        pass


    # Enter a parse tree produced by gnfdParser#left.
    def enterLeft(self, ctx:gnfdParser.LeftContext):
        pass

    # Exit a parse tree produced by gnfdParser#left.
    def exitLeft(self, ctx:gnfdParser.LeftContext):
        pass


    # Enter a parse tree produced by gnfdParser#right.
    def enterRight(self, ctx:gnfdParser.RightContext):
        pass

    # Exit a parse tree produced by gnfdParser#right.
    def exitRight(self, ctx:gnfdParser.RightContext):
        pass


    # Enter a parse tree produced by gnfdParser#reference.
    def enterReference(self, ctx:gnfdParser.ReferenceContext):
        pass

    # Exit a parse tree produced by gnfdParser#reference.
    def exitReference(self, ctx:gnfdParser.ReferenceContext):
        pass


    # Enter a parse tree produced by gnfdParser#property.
    def enterProperty(self, ctx:gnfdParser.PropertyContext):
        pass

    # Exit a parse tree produced by gnfdParser#property.
    def exitProperty(self, ctx:gnfdParser.PropertyContext):
        pass


    # Enter a parse tree produced by gnfdParser#pattern.
    def enterPattern(self, ctx:gnfdParser.PatternContext):
        pass

    # Exit a parse tree produced by gnfdParser#pattern.
    def exitPattern(self, ctx:gnfdParser.PatternContext):
        pass


    # Enter a parse tree produced by gnfdParser#labelList.
    def enterLabelList(self, ctx:gnfdParser.LabelListContext):
        pass

    # Exit a parse tree produced by gnfdParser#labelList.
    def exitLabelList(self, ctx:gnfdParser.LabelListContext):
        pass


    # Enter a parse tree produced by gnfdParser#propertyList.
    def enterPropertyList(self, ctx:gnfdParser.PropertyListContext):
        pass

    # Exit a parse tree produced by gnfdParser#propertyList.
    def exitPropertyList(self, ctx:gnfdParser.PropertyListContext):
        pass


    # Enter a parse tree produced by gnfdParser#label.
    def enterLabel(self, ctx:gnfdParser.LabelContext):
        pass

    # Exit a parse tree produced by gnfdParser#label.
    def exitLabel(self, ctx:gnfdParser.LabelContext):
        pass


    # Enter a parse tree produced by gnfdParser#varName.
    def enterVarName(self, ctx:gnfdParser.VarNameContext):
        pass

    # Exit a parse tree produced by gnfdParser#varName.
    def exitVarName(self, ctx:gnfdParser.VarNameContext):
        pass


    # Enter a parse tree produced by gnfdParser#propertyKey.
    def enterPropertyKey(self, ctx:gnfdParser.PropertyKeyContext):
        pass

    # Exit a parse tree produced by gnfdParser#propertyKey.
    def exitPropertyKey(self, ctx:gnfdParser.PropertyKeyContext):
        pass


    # Enter a parse tree produced by gnfdParser#nodePattern.
    def enterNodePattern(self, ctx:gnfdParser.NodePatternContext):
        pass

    # Exit a parse tree produced by gnfdParser#nodePattern.
    def exitNodePattern(self, ctx:gnfdParser.NodePatternContext):
        pass



del gnfdParser