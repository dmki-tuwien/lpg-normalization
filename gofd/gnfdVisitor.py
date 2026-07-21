# Generated from gnfd.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gnfdParser import gnfdParser
else:
    from gnfdParser import gnfdParser

# This class defines a complete generic visitor for a parse tree produced by gnfdParser.

class gnfdVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gnfdParser#dependency.
    def visitDependency(self, ctx:gnfdParser.DependencyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#left.
    def visitLeft(self, ctx:gnfdParser.LeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#right.
    def visitRight(self, ctx:gnfdParser.RightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#reference.
    def visitReference(self, ctx:gnfdParser.ReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#property.
    def visitProperty(self, ctx:gnfdParser.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#pattern.
    def visitPattern(self, ctx:gnfdParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#labelList.
    def visitLabelList(self, ctx:gnfdParser.LabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#propertyList.
    def visitPropertyList(self, ctx:gnfdParser.PropertyListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#label.
    def visitLabel(self, ctx:gnfdParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#varName.
    def visitVarName(self, ctx:gnfdParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#propertyKey.
    def visitPropertyKey(self, ctx:gnfdParser.PropertyKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#nodePattern.
    def visitNodePattern(self, ctx:gnfdParser.NodePatternContext):
        return self.visitChildren(ctx)



del gnfdParser