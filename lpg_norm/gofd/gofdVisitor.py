# Generated from gnfd.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gnfdParser import gofdParser
else:
    from gnfdParser import gofdParser

# This class defines a complete generic visitor for a parse tree produced by gnfdParser.

class gnfdVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gnfdParser#dependency.
    def visitDependency(self, ctx:gofdParser.DependencyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#left.
    def visitLeft(self, ctx:gofdParser.LeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#right.
    def visitRight(self, ctx:gofdParser.RightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#reference.
    def visitReference(self, ctx:gofdParser.ReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#property.
    def visitProperty(self, ctx:gofdParser.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#pattern.
    def visitPattern(self, ctx:gofdParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#labelList.
    def visitLabelList(self, ctx:gofdParser.LabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#propertyList.
    def visitPropertyList(self, ctx:gofdParser.PropertyListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#label.
    def visitLabel(self, ctx:gofdParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#varName.
    def visitVarName(self, ctx:gofdParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#propertyKey.
    def visitPropertyKey(self, ctx:gofdParser.PropertyKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gnfdParser#nodePattern.
    def visitNodePattern(self, ctx:gofdParser.NodePatternContext):
        return self.visitChildren(ctx)



del gofdParser