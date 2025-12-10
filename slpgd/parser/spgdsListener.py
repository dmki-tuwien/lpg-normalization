# Generated from spgds.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .spgdsParser import spgdsParser
else:
    from spgdsParser import spgdsParser

# This class defines a complete listener for a parse tree produced by spgdsParser.
class spgdsListener(ParseTreeListener):

    # Enter a parse tree produced by spgdsParser#dependency.
    def enterDependency(self, ctx:spgdsParser.DependencyContext):
        pass

    # Exit a parse tree produced by spgdsParser#dependency.
    def exitDependency(self, ctx:spgdsParser.DependencyContext):
        pass


    # Enter a parse tree produced by spgdsParser#left.
    def enterLeft(self, ctx:spgdsParser.LeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#left.
    def exitLeft(self, ctx:spgdsParser.LeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#right.
    def enterRight(self, ctx:spgdsParser.RightContext):
        pass

    # Exit a parse tree produced by spgdsParser#right.
    def exitRight(self, ctx:spgdsParser.RightContext):
        pass


    # Enter a parse tree produced by spgdsParser#reference.
    def enterReference(self, ctx:spgdsParser.ReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#reference.
    def exitReference(self, ctx:spgdsParser.ReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#gqlProgram.
    def enterGqlProgram(self, ctx:spgdsParser.GqlProgramContext):
        pass

    # Exit a parse tree produced by spgdsParser#gqlProgram.
    def exitGqlProgram(self, ctx:spgdsParser.GqlProgramContext):
        pass


    # Enter a parse tree produced by spgdsParser#programActivity.
    def enterProgramActivity(self, ctx:spgdsParser.ProgramActivityContext):
        pass

    # Exit a parse tree produced by spgdsParser#programActivity.
    def exitProgramActivity(self, ctx:spgdsParser.ProgramActivityContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionActivity.
    def enterSessionActivity(self, ctx:spgdsParser.SessionActivityContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionActivity.
    def exitSessionActivity(self, ctx:spgdsParser.SessionActivityContext):
        pass


    # Enter a parse tree produced by spgdsParser#transactionActivity.
    def enterTransactionActivity(self, ctx:spgdsParser.TransactionActivityContext):
        pass

    # Exit a parse tree produced by spgdsParser#transactionActivity.
    def exitTransactionActivity(self, ctx:spgdsParser.TransactionActivityContext):
        pass


    # Enter a parse tree produced by spgdsParser#endTransactionCommand.
    def enterEndTransactionCommand(self, ctx:spgdsParser.EndTransactionCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#endTransactionCommand.
    def exitEndTransactionCommand(self, ctx:spgdsParser.EndTransactionCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetCommand.
    def enterSessionSetCommand(self, ctx:spgdsParser.SessionSetCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetCommand.
    def exitSessionSetCommand(self, ctx:spgdsParser.SessionSetCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetSchemaClause.
    def enterSessionSetSchemaClause(self, ctx:spgdsParser.SessionSetSchemaClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetSchemaClause.
    def exitSessionSetSchemaClause(self, ctx:spgdsParser.SessionSetSchemaClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetGraphClause.
    def enterSessionSetGraphClause(self, ctx:spgdsParser.SessionSetGraphClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetGraphClause.
    def exitSessionSetGraphClause(self, ctx:spgdsParser.SessionSetGraphClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetTimeZoneClause.
    def enterSessionSetTimeZoneClause(self, ctx:spgdsParser.SessionSetTimeZoneClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetTimeZoneClause.
    def exitSessionSetTimeZoneClause(self, ctx:spgdsParser.SessionSetTimeZoneClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#setTimeZoneValue.
    def enterSetTimeZoneValue(self, ctx:spgdsParser.SetTimeZoneValueContext):
        pass

    # Exit a parse tree produced by spgdsParser#setTimeZoneValue.
    def exitSetTimeZoneValue(self, ctx:spgdsParser.SetTimeZoneValueContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetParameterClause.
    def enterSessionSetParameterClause(self, ctx:spgdsParser.SessionSetParameterClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetParameterClause.
    def exitSessionSetParameterClause(self, ctx:spgdsParser.SessionSetParameterClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetGraphParameterClause.
    def enterSessionSetGraphParameterClause(self, ctx:spgdsParser.SessionSetGraphParameterClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetGraphParameterClause.
    def exitSessionSetGraphParameterClause(self, ctx:spgdsParser.SessionSetGraphParameterClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetBindingTableParameterClause.
    def enterSessionSetBindingTableParameterClause(self, ctx:spgdsParser.SessionSetBindingTableParameterClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetBindingTableParameterClause.
    def exitSessionSetBindingTableParameterClause(self, ctx:spgdsParser.SessionSetBindingTableParameterClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetValueParameterClause.
    def enterSessionSetValueParameterClause(self, ctx:spgdsParser.SessionSetValueParameterClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetValueParameterClause.
    def exitSessionSetValueParameterClause(self, ctx:spgdsParser.SessionSetValueParameterClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionSetParameterName.
    def enterSessionSetParameterName(self, ctx:spgdsParser.SessionSetParameterNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionSetParameterName.
    def exitSessionSetParameterName(self, ctx:spgdsParser.SessionSetParameterNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionResetCommand.
    def enterSessionResetCommand(self, ctx:spgdsParser.SessionResetCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionResetCommand.
    def exitSessionResetCommand(self, ctx:spgdsParser.SessionResetCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionResetArguments.
    def enterSessionResetArguments(self, ctx:spgdsParser.SessionResetArgumentsContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionResetArguments.
    def exitSessionResetArguments(self, ctx:spgdsParser.SessionResetArgumentsContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionCloseCommand.
    def enterSessionCloseCommand(self, ctx:spgdsParser.SessionCloseCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionCloseCommand.
    def exitSessionCloseCommand(self, ctx:spgdsParser.SessionCloseCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#sessionParameterSpecification.
    def enterSessionParameterSpecification(self, ctx:spgdsParser.SessionParameterSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#sessionParameterSpecification.
    def exitSessionParameterSpecification(self, ctx:spgdsParser.SessionParameterSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#startTransactionCommand.
    def enterStartTransactionCommand(self, ctx:spgdsParser.StartTransactionCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#startTransactionCommand.
    def exitStartTransactionCommand(self, ctx:spgdsParser.StartTransactionCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#transactionCharacteristics.
    def enterTransactionCharacteristics(self, ctx:spgdsParser.TransactionCharacteristicsContext):
        pass

    # Exit a parse tree produced by spgdsParser#transactionCharacteristics.
    def exitTransactionCharacteristics(self, ctx:spgdsParser.TransactionCharacteristicsContext):
        pass


    # Enter a parse tree produced by spgdsParser#transactionMode.
    def enterTransactionMode(self, ctx:spgdsParser.TransactionModeContext):
        pass

    # Exit a parse tree produced by spgdsParser#transactionMode.
    def exitTransactionMode(self, ctx:spgdsParser.TransactionModeContext):
        pass


    # Enter a parse tree produced by spgdsParser#transactionAccessMode.
    def enterTransactionAccessMode(self, ctx:spgdsParser.TransactionAccessModeContext):
        pass

    # Exit a parse tree produced by spgdsParser#transactionAccessMode.
    def exitTransactionAccessMode(self, ctx:spgdsParser.TransactionAccessModeContext):
        pass


    # Enter a parse tree produced by spgdsParser#rollbackCommand.
    def enterRollbackCommand(self, ctx:spgdsParser.RollbackCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#rollbackCommand.
    def exitRollbackCommand(self, ctx:spgdsParser.RollbackCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#commitCommand.
    def enterCommitCommand(self, ctx:spgdsParser.CommitCommandContext):
        pass

    # Exit a parse tree produced by spgdsParser#commitCommand.
    def exitCommitCommand(self, ctx:spgdsParser.CommitCommandContext):
        pass


    # Enter a parse tree produced by spgdsParser#nestedProcedureSpecification.
    def enterNestedProcedureSpecification(self, ctx:spgdsParser.NestedProcedureSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nestedProcedureSpecification.
    def exitNestedProcedureSpecification(self, ctx:spgdsParser.NestedProcedureSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureSpecification.
    def enterProcedureSpecification(self, ctx:spgdsParser.ProcedureSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureSpecification.
    def exitProcedureSpecification(self, ctx:spgdsParser.ProcedureSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nestedDataModifyingProcedureSpecification.
    def enterNestedDataModifyingProcedureSpecification(self, ctx:spgdsParser.NestedDataModifyingProcedureSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nestedDataModifyingProcedureSpecification.
    def exitNestedDataModifyingProcedureSpecification(self, ctx:spgdsParser.NestedDataModifyingProcedureSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nestedQuerySpecification.
    def enterNestedQuerySpecification(self, ctx:spgdsParser.NestedQuerySpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nestedQuerySpecification.
    def exitNestedQuerySpecification(self, ctx:spgdsParser.NestedQuerySpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureBody.
    def enterProcedureBody(self, ctx:spgdsParser.ProcedureBodyContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureBody.
    def exitProcedureBody(self, ctx:spgdsParser.ProcedureBodyContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingVariableDefinitionBlock.
    def enterBindingVariableDefinitionBlock(self, ctx:spgdsParser.BindingVariableDefinitionBlockContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingVariableDefinitionBlock.
    def exitBindingVariableDefinitionBlock(self, ctx:spgdsParser.BindingVariableDefinitionBlockContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingVariableDefinition.
    def enterBindingVariableDefinition(self, ctx:spgdsParser.BindingVariableDefinitionContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingVariableDefinition.
    def exitBindingVariableDefinition(self, ctx:spgdsParser.BindingVariableDefinitionContext):
        pass


    # Enter a parse tree produced by spgdsParser#statementBlock.
    def enterStatementBlock(self, ctx:spgdsParser.StatementBlockContext):
        pass

    # Exit a parse tree produced by spgdsParser#statementBlock.
    def exitStatementBlock(self, ctx:spgdsParser.StatementBlockContext):
        pass


    # Enter a parse tree produced by spgdsParser#statement.
    def enterStatement(self, ctx:spgdsParser.StatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#statement.
    def exitStatement(self, ctx:spgdsParser.StatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#nextStatement.
    def enterNextStatement(self, ctx:spgdsParser.NextStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#nextStatement.
    def exitNextStatement(self, ctx:spgdsParser.NextStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphVariableDefinition.
    def enterGraphVariableDefinition(self, ctx:spgdsParser.GraphVariableDefinitionContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphVariableDefinition.
    def exitGraphVariableDefinition(self, ctx:spgdsParser.GraphVariableDefinitionContext):
        pass


    # Enter a parse tree produced by spgdsParser#optTypedGraphInitializer.
    def enterOptTypedGraphInitializer(self, ctx:spgdsParser.OptTypedGraphInitializerContext):
        pass

    # Exit a parse tree produced by spgdsParser#optTypedGraphInitializer.
    def exitOptTypedGraphInitializer(self, ctx:spgdsParser.OptTypedGraphInitializerContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphInitializer.
    def enterGraphInitializer(self, ctx:spgdsParser.GraphInitializerContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphInitializer.
    def exitGraphInitializer(self, ctx:spgdsParser.GraphInitializerContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableVariableDefinition.
    def enterBindingTableVariableDefinition(self, ctx:spgdsParser.BindingTableVariableDefinitionContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableVariableDefinition.
    def exitBindingTableVariableDefinition(self, ctx:spgdsParser.BindingTableVariableDefinitionContext):
        pass


    # Enter a parse tree produced by spgdsParser#optTypedBindingTableInitializer.
    def enterOptTypedBindingTableInitializer(self, ctx:spgdsParser.OptTypedBindingTableInitializerContext):
        pass

    # Exit a parse tree produced by spgdsParser#optTypedBindingTableInitializer.
    def exitOptTypedBindingTableInitializer(self, ctx:spgdsParser.OptTypedBindingTableInitializerContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableInitializer.
    def enterBindingTableInitializer(self, ctx:spgdsParser.BindingTableInitializerContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableInitializer.
    def exitBindingTableInitializer(self, ctx:spgdsParser.BindingTableInitializerContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueVariableDefinition.
    def enterValueVariableDefinition(self, ctx:spgdsParser.ValueVariableDefinitionContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueVariableDefinition.
    def exitValueVariableDefinition(self, ctx:spgdsParser.ValueVariableDefinitionContext):
        pass


    # Enter a parse tree produced by spgdsParser#optTypedValueInitializer.
    def enterOptTypedValueInitializer(self, ctx:spgdsParser.OptTypedValueInitializerContext):
        pass

    # Exit a parse tree produced by spgdsParser#optTypedValueInitializer.
    def exitOptTypedValueInitializer(self, ctx:spgdsParser.OptTypedValueInitializerContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueInitializer.
    def enterValueInitializer(self, ctx:spgdsParser.ValueInitializerContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueInitializer.
    def exitValueInitializer(self, ctx:spgdsParser.ValueInitializerContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphExpression.
    def enterGraphExpression(self, ctx:spgdsParser.GraphExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphExpression.
    def exitGraphExpression(self, ctx:spgdsParser.GraphExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#currentGraph.
    def enterCurrentGraph(self, ctx:spgdsParser.CurrentGraphContext):
        pass

    # Exit a parse tree produced by spgdsParser#currentGraph.
    def exitCurrentGraph(self, ctx:spgdsParser.CurrentGraphContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableExpression.
    def enterBindingTableExpression(self, ctx:spgdsParser.BindingTableExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableExpression.
    def exitBindingTableExpression(self, ctx:spgdsParser.BindingTableExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#nestedBindingTableQuerySpecification.
    def enterNestedBindingTableQuerySpecification(self, ctx:spgdsParser.NestedBindingTableQuerySpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nestedBindingTableQuerySpecification.
    def exitNestedBindingTableQuerySpecification(self, ctx:spgdsParser.NestedBindingTableQuerySpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#objectExpressionPrimary.
    def enterObjectExpressionPrimary(self, ctx:spgdsParser.ObjectExpressionPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#objectExpressionPrimary.
    def exitObjectExpressionPrimary(self, ctx:spgdsParser.ObjectExpressionPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#linearCatalogModifyingStatement.
    def enterLinearCatalogModifyingStatement(self, ctx:spgdsParser.LinearCatalogModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#linearCatalogModifyingStatement.
    def exitLinearCatalogModifyingStatement(self, ctx:spgdsParser.LinearCatalogModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleCatalogModifyingStatement.
    def enterSimpleCatalogModifyingStatement(self, ctx:spgdsParser.SimpleCatalogModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleCatalogModifyingStatement.
    def exitSimpleCatalogModifyingStatement(self, ctx:spgdsParser.SimpleCatalogModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#primitiveCatalogModifyingStatement.
    def enterPrimitiveCatalogModifyingStatement(self, ctx:spgdsParser.PrimitiveCatalogModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#primitiveCatalogModifyingStatement.
    def exitPrimitiveCatalogModifyingStatement(self, ctx:spgdsParser.PrimitiveCatalogModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#createSchemaStatement.
    def enterCreateSchemaStatement(self, ctx:spgdsParser.CreateSchemaStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#createSchemaStatement.
    def exitCreateSchemaStatement(self, ctx:spgdsParser.CreateSchemaStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#dropSchemaStatement.
    def enterDropSchemaStatement(self, ctx:spgdsParser.DropSchemaStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#dropSchemaStatement.
    def exitDropSchemaStatement(self, ctx:spgdsParser.DropSchemaStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#createGraphStatement.
    def enterCreateGraphStatement(self, ctx:spgdsParser.CreateGraphStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#createGraphStatement.
    def exitCreateGraphStatement(self, ctx:spgdsParser.CreateGraphStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#openGraphType.
    def enterOpenGraphType(self, ctx:spgdsParser.OpenGraphTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#openGraphType.
    def exitOpenGraphType(self, ctx:spgdsParser.OpenGraphTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#ofGraphType.
    def enterOfGraphType(self, ctx:spgdsParser.OfGraphTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#ofGraphType.
    def exitOfGraphType(self, ctx:spgdsParser.OfGraphTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphTypeLikeGraph.
    def enterGraphTypeLikeGraph(self, ctx:spgdsParser.GraphTypeLikeGraphContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphTypeLikeGraph.
    def exitGraphTypeLikeGraph(self, ctx:spgdsParser.GraphTypeLikeGraphContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphSource.
    def enterGraphSource(self, ctx:spgdsParser.GraphSourceContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphSource.
    def exitGraphSource(self, ctx:spgdsParser.GraphSourceContext):
        pass


    # Enter a parse tree produced by spgdsParser#dropGraphStatement.
    def enterDropGraphStatement(self, ctx:spgdsParser.DropGraphStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#dropGraphStatement.
    def exitDropGraphStatement(self, ctx:spgdsParser.DropGraphStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#createGraphTypeStatement.
    def enterCreateGraphTypeStatement(self, ctx:spgdsParser.CreateGraphTypeStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#createGraphTypeStatement.
    def exitCreateGraphTypeStatement(self, ctx:spgdsParser.CreateGraphTypeStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphTypeSource.
    def enterGraphTypeSource(self, ctx:spgdsParser.GraphTypeSourceContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphTypeSource.
    def exitGraphTypeSource(self, ctx:spgdsParser.GraphTypeSourceContext):
        pass


    # Enter a parse tree produced by spgdsParser#copyOfGraphType.
    def enterCopyOfGraphType(self, ctx:spgdsParser.CopyOfGraphTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#copyOfGraphType.
    def exitCopyOfGraphType(self, ctx:spgdsParser.CopyOfGraphTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#dropGraphTypeStatement.
    def enterDropGraphTypeStatement(self, ctx:spgdsParser.DropGraphTypeStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#dropGraphTypeStatement.
    def exitDropGraphTypeStatement(self, ctx:spgdsParser.DropGraphTypeStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#callCatalogModifyingProcedureStatement.
    def enterCallCatalogModifyingProcedureStatement(self, ctx:spgdsParser.CallCatalogModifyingProcedureStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#callCatalogModifyingProcedureStatement.
    def exitCallCatalogModifyingProcedureStatement(self, ctx:spgdsParser.CallCatalogModifyingProcedureStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#linearDataModifyingStatement.
    def enterLinearDataModifyingStatement(self, ctx:spgdsParser.LinearDataModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#linearDataModifyingStatement.
    def exitLinearDataModifyingStatement(self, ctx:spgdsParser.LinearDataModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedLinearDataModifyingStatement.
    def enterFocusedLinearDataModifyingStatement(self, ctx:spgdsParser.FocusedLinearDataModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedLinearDataModifyingStatement.
    def exitFocusedLinearDataModifyingStatement(self, ctx:spgdsParser.FocusedLinearDataModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedLinearDataModifyingStatementBody.
    def enterFocusedLinearDataModifyingStatementBody(self, ctx:spgdsParser.FocusedLinearDataModifyingStatementBodyContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedLinearDataModifyingStatementBody.
    def exitFocusedLinearDataModifyingStatementBody(self, ctx:spgdsParser.FocusedLinearDataModifyingStatementBodyContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedNestedDataModifyingProcedureSpecification.
    def enterFocusedNestedDataModifyingProcedureSpecification(self, ctx:spgdsParser.FocusedNestedDataModifyingProcedureSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedNestedDataModifyingProcedureSpecification.
    def exitFocusedNestedDataModifyingProcedureSpecification(self, ctx:spgdsParser.FocusedNestedDataModifyingProcedureSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#ambientLinearDataModifyingStatement.
    def enterAmbientLinearDataModifyingStatement(self, ctx:spgdsParser.AmbientLinearDataModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#ambientLinearDataModifyingStatement.
    def exitAmbientLinearDataModifyingStatement(self, ctx:spgdsParser.AmbientLinearDataModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#ambientLinearDataModifyingStatementBody.
    def enterAmbientLinearDataModifyingStatementBody(self, ctx:spgdsParser.AmbientLinearDataModifyingStatementBodyContext):
        pass

    # Exit a parse tree produced by spgdsParser#ambientLinearDataModifyingStatementBody.
    def exitAmbientLinearDataModifyingStatementBody(self, ctx:spgdsParser.AmbientLinearDataModifyingStatementBodyContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleLinearDataAccessingStatement.
    def enterSimpleLinearDataAccessingStatement(self, ctx:spgdsParser.SimpleLinearDataAccessingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleLinearDataAccessingStatement.
    def exitSimpleLinearDataAccessingStatement(self, ctx:spgdsParser.SimpleLinearDataAccessingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleDataAccessingStatement.
    def enterSimpleDataAccessingStatement(self, ctx:spgdsParser.SimpleDataAccessingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleDataAccessingStatement.
    def exitSimpleDataAccessingStatement(self, ctx:spgdsParser.SimpleDataAccessingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleDataModifyingStatement.
    def enterSimpleDataModifyingStatement(self, ctx:spgdsParser.SimpleDataModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleDataModifyingStatement.
    def exitSimpleDataModifyingStatement(self, ctx:spgdsParser.SimpleDataModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#primitiveDataModifyingStatement.
    def enterPrimitiveDataModifyingStatement(self, ctx:spgdsParser.PrimitiveDataModifyingStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#primitiveDataModifyingStatement.
    def exitPrimitiveDataModifyingStatement(self, ctx:spgdsParser.PrimitiveDataModifyingStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertStatement.
    def enterInsertStatement(self, ctx:spgdsParser.InsertStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertStatement.
    def exitInsertStatement(self, ctx:spgdsParser.InsertStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#setStatement.
    def enterSetStatement(self, ctx:spgdsParser.SetStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#setStatement.
    def exitSetStatement(self, ctx:spgdsParser.SetStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#setItemList.
    def enterSetItemList(self, ctx:spgdsParser.SetItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#setItemList.
    def exitSetItemList(self, ctx:spgdsParser.SetItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#setItem.
    def enterSetItem(self, ctx:spgdsParser.SetItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#setItem.
    def exitSetItem(self, ctx:spgdsParser.SetItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#setPropertyItem.
    def enterSetPropertyItem(self, ctx:spgdsParser.SetPropertyItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#setPropertyItem.
    def exitSetPropertyItem(self, ctx:spgdsParser.SetPropertyItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#setAllPropertiesItem.
    def enterSetAllPropertiesItem(self, ctx:spgdsParser.SetAllPropertiesItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#setAllPropertiesItem.
    def exitSetAllPropertiesItem(self, ctx:spgdsParser.SetAllPropertiesItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#setLabelItem.
    def enterSetLabelItem(self, ctx:spgdsParser.SetLabelItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#setLabelItem.
    def exitSetLabelItem(self, ctx:spgdsParser.SetLabelItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#removeStatement.
    def enterRemoveStatement(self, ctx:spgdsParser.RemoveStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#removeStatement.
    def exitRemoveStatement(self, ctx:spgdsParser.RemoveStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#removeItemList.
    def enterRemoveItemList(self, ctx:spgdsParser.RemoveItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#removeItemList.
    def exitRemoveItemList(self, ctx:spgdsParser.RemoveItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#removeItem.
    def enterRemoveItem(self, ctx:spgdsParser.RemoveItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#removeItem.
    def exitRemoveItem(self, ctx:spgdsParser.RemoveItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#removePropertyItem.
    def enterRemovePropertyItem(self, ctx:spgdsParser.RemovePropertyItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#removePropertyItem.
    def exitRemovePropertyItem(self, ctx:spgdsParser.RemovePropertyItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#removeLabelItem.
    def enterRemoveLabelItem(self, ctx:spgdsParser.RemoveLabelItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#removeLabelItem.
    def exitRemoveLabelItem(self, ctx:spgdsParser.RemoveLabelItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#deleteStatement.
    def enterDeleteStatement(self, ctx:spgdsParser.DeleteStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#deleteStatement.
    def exitDeleteStatement(self, ctx:spgdsParser.DeleteStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#deleteItemList.
    def enterDeleteItemList(self, ctx:spgdsParser.DeleteItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#deleteItemList.
    def exitDeleteItemList(self, ctx:spgdsParser.DeleteItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#deleteItem.
    def enterDeleteItem(self, ctx:spgdsParser.DeleteItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#deleteItem.
    def exitDeleteItem(self, ctx:spgdsParser.DeleteItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#callDataModifyingProcedureStatement.
    def enterCallDataModifyingProcedureStatement(self, ctx:spgdsParser.CallDataModifyingProcedureStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#callDataModifyingProcedureStatement.
    def exitCallDataModifyingProcedureStatement(self, ctx:spgdsParser.CallDataModifyingProcedureStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#compositeQueryStatement.
    def enterCompositeQueryStatement(self, ctx:spgdsParser.CompositeQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#compositeQueryStatement.
    def exitCompositeQueryStatement(self, ctx:spgdsParser.CompositeQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#compositeQueryExpression.
    def enterCompositeQueryExpression(self, ctx:spgdsParser.CompositeQueryExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#compositeQueryExpression.
    def exitCompositeQueryExpression(self, ctx:spgdsParser.CompositeQueryExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#queryConjunction.
    def enterQueryConjunction(self, ctx:spgdsParser.QueryConjunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#queryConjunction.
    def exitQueryConjunction(self, ctx:spgdsParser.QueryConjunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#setOperator.
    def enterSetOperator(self, ctx:spgdsParser.SetOperatorContext):
        pass

    # Exit a parse tree produced by spgdsParser#setOperator.
    def exitSetOperator(self, ctx:spgdsParser.SetOperatorContext):
        pass


    # Enter a parse tree produced by spgdsParser#compositeQueryPrimary.
    def enterCompositeQueryPrimary(self, ctx:spgdsParser.CompositeQueryPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#compositeQueryPrimary.
    def exitCompositeQueryPrimary(self, ctx:spgdsParser.CompositeQueryPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#linearQueryStatement.
    def enterLinearQueryStatement(self, ctx:spgdsParser.LinearQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#linearQueryStatement.
    def exitLinearQueryStatement(self, ctx:spgdsParser.LinearQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedLinearQueryStatement.
    def enterFocusedLinearQueryStatement(self, ctx:spgdsParser.FocusedLinearQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedLinearQueryStatement.
    def exitFocusedLinearQueryStatement(self, ctx:spgdsParser.FocusedLinearQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedLinearQueryStatementPart.
    def enterFocusedLinearQueryStatementPart(self, ctx:spgdsParser.FocusedLinearQueryStatementPartContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedLinearQueryStatementPart.
    def exitFocusedLinearQueryStatementPart(self, ctx:spgdsParser.FocusedLinearQueryStatementPartContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedLinearQueryAndPrimitiveResultStatementPart.
    def enterFocusedLinearQueryAndPrimitiveResultStatementPart(self, ctx:spgdsParser.FocusedLinearQueryAndPrimitiveResultStatementPartContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedLinearQueryAndPrimitiveResultStatementPart.
    def exitFocusedLinearQueryAndPrimitiveResultStatementPart(self, ctx:spgdsParser.FocusedLinearQueryAndPrimitiveResultStatementPartContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedPrimitiveResultStatement.
    def enterFocusedPrimitiveResultStatement(self, ctx:spgdsParser.FocusedPrimitiveResultStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedPrimitiveResultStatement.
    def exitFocusedPrimitiveResultStatement(self, ctx:spgdsParser.FocusedPrimitiveResultStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#focusedNestedQuerySpecification.
    def enterFocusedNestedQuerySpecification(self, ctx:spgdsParser.FocusedNestedQuerySpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#focusedNestedQuerySpecification.
    def exitFocusedNestedQuerySpecification(self, ctx:spgdsParser.FocusedNestedQuerySpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#ambientLinearQueryStatement.
    def enterAmbientLinearQueryStatement(self, ctx:spgdsParser.AmbientLinearQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#ambientLinearQueryStatement.
    def exitAmbientLinearQueryStatement(self, ctx:spgdsParser.AmbientLinearQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleLinearQueryStatement.
    def enterSimpleLinearQueryStatement(self, ctx:spgdsParser.SimpleLinearQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleLinearQueryStatement.
    def exitSimpleLinearQueryStatement(self, ctx:spgdsParser.SimpleLinearQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleQueryStatement.
    def enterSimpleQueryStatement(self, ctx:spgdsParser.SimpleQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleQueryStatement.
    def exitSimpleQueryStatement(self, ctx:spgdsParser.SimpleQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#primitiveQueryStatement.
    def enterPrimitiveQueryStatement(self, ctx:spgdsParser.PrimitiveQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#primitiveQueryStatement.
    def exitPrimitiveQueryStatement(self, ctx:spgdsParser.PrimitiveQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#matchStatement.
    def enterMatchStatement(self, ctx:spgdsParser.MatchStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#matchStatement.
    def exitMatchStatement(self, ctx:spgdsParser.MatchStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleMatchStatement.
    def enterSimpleMatchStatement(self, ctx:spgdsParser.SimpleMatchStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleMatchStatement.
    def exitSimpleMatchStatement(self, ctx:spgdsParser.SimpleMatchStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#optionalMatchStatement.
    def enterOptionalMatchStatement(self, ctx:spgdsParser.OptionalMatchStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#optionalMatchStatement.
    def exitOptionalMatchStatement(self, ctx:spgdsParser.OptionalMatchStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#optionalOperand.
    def enterOptionalOperand(self, ctx:spgdsParser.OptionalOperandContext):
        pass

    # Exit a parse tree produced by spgdsParser#optionalOperand.
    def exitOptionalOperand(self, ctx:spgdsParser.OptionalOperandContext):
        pass


    # Enter a parse tree produced by spgdsParser#matchStatementBlock.
    def enterMatchStatementBlock(self, ctx:spgdsParser.MatchStatementBlockContext):
        pass

    # Exit a parse tree produced by spgdsParser#matchStatementBlock.
    def exitMatchStatementBlock(self, ctx:spgdsParser.MatchStatementBlockContext):
        pass


    # Enter a parse tree produced by spgdsParser#callQueryStatement.
    def enterCallQueryStatement(self, ctx:spgdsParser.CallQueryStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#callQueryStatement.
    def exitCallQueryStatement(self, ctx:spgdsParser.CallQueryStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#filterStatement.
    def enterFilterStatement(self, ctx:spgdsParser.FilterStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#filterStatement.
    def exitFilterStatement(self, ctx:spgdsParser.FilterStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#letStatement.
    def enterLetStatement(self, ctx:spgdsParser.LetStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#letStatement.
    def exitLetStatement(self, ctx:spgdsParser.LetStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#letVariableDefinitionList.
    def enterLetVariableDefinitionList(self, ctx:spgdsParser.LetVariableDefinitionListContext):
        pass

    # Exit a parse tree produced by spgdsParser#letVariableDefinitionList.
    def exitLetVariableDefinitionList(self, ctx:spgdsParser.LetVariableDefinitionListContext):
        pass


    # Enter a parse tree produced by spgdsParser#letVariableDefinition.
    def enterLetVariableDefinition(self, ctx:spgdsParser.LetVariableDefinitionContext):
        pass

    # Exit a parse tree produced by spgdsParser#letVariableDefinition.
    def exitLetVariableDefinition(self, ctx:spgdsParser.LetVariableDefinitionContext):
        pass


    # Enter a parse tree produced by spgdsParser#forStatement.
    def enterForStatement(self, ctx:spgdsParser.ForStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#forStatement.
    def exitForStatement(self, ctx:spgdsParser.ForStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#forItem.
    def enterForItem(self, ctx:spgdsParser.ForItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#forItem.
    def exitForItem(self, ctx:spgdsParser.ForItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#forItemAlias.
    def enterForItemAlias(self, ctx:spgdsParser.ForItemAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#forItemAlias.
    def exitForItemAlias(self, ctx:spgdsParser.ForItemAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#forItemSource.
    def enterForItemSource(self, ctx:spgdsParser.ForItemSourceContext):
        pass

    # Exit a parse tree produced by spgdsParser#forItemSource.
    def exitForItemSource(self, ctx:spgdsParser.ForItemSourceContext):
        pass


    # Enter a parse tree produced by spgdsParser#forOrdinalityOrOffset.
    def enterForOrdinalityOrOffset(self, ctx:spgdsParser.ForOrdinalityOrOffsetContext):
        pass

    # Exit a parse tree produced by spgdsParser#forOrdinalityOrOffset.
    def exitForOrdinalityOrOffset(self, ctx:spgdsParser.ForOrdinalityOrOffsetContext):
        pass


    # Enter a parse tree produced by spgdsParser#orderByAndPageStatement.
    def enterOrderByAndPageStatement(self, ctx:spgdsParser.OrderByAndPageStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#orderByAndPageStatement.
    def exitOrderByAndPageStatement(self, ctx:spgdsParser.OrderByAndPageStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#primitiveResultStatement.
    def enterPrimitiveResultStatement(self, ctx:spgdsParser.PrimitiveResultStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#primitiveResultStatement.
    def exitPrimitiveResultStatement(self, ctx:spgdsParser.PrimitiveResultStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#returnStatement.
    def enterReturnStatement(self, ctx:spgdsParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#returnStatement.
    def exitReturnStatement(self, ctx:spgdsParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#returnStatementBody.
    def enterReturnStatementBody(self, ctx:spgdsParser.ReturnStatementBodyContext):
        pass

    # Exit a parse tree produced by spgdsParser#returnStatementBody.
    def exitReturnStatementBody(self, ctx:spgdsParser.ReturnStatementBodyContext):
        pass


    # Enter a parse tree produced by spgdsParser#returnItemList.
    def enterReturnItemList(self, ctx:spgdsParser.ReturnItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#returnItemList.
    def exitReturnItemList(self, ctx:spgdsParser.ReturnItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#returnItem.
    def enterReturnItem(self, ctx:spgdsParser.ReturnItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#returnItem.
    def exitReturnItem(self, ctx:spgdsParser.ReturnItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#returnItemAlias.
    def enterReturnItemAlias(self, ctx:spgdsParser.ReturnItemAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#returnItemAlias.
    def exitReturnItemAlias(self, ctx:spgdsParser.ReturnItemAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectStatement.
    def enterSelectStatement(self, ctx:spgdsParser.SelectStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectStatement.
    def exitSelectStatement(self, ctx:spgdsParser.SelectStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectItemList.
    def enterSelectItemList(self, ctx:spgdsParser.SelectItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectItemList.
    def exitSelectItemList(self, ctx:spgdsParser.SelectItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectItem.
    def enterSelectItem(self, ctx:spgdsParser.SelectItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectItem.
    def exitSelectItem(self, ctx:spgdsParser.SelectItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectItemAlias.
    def enterSelectItemAlias(self, ctx:spgdsParser.SelectItemAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectItemAlias.
    def exitSelectItemAlias(self, ctx:spgdsParser.SelectItemAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#havingClause.
    def enterHavingClause(self, ctx:spgdsParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#havingClause.
    def exitHavingClause(self, ctx:spgdsParser.HavingClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectStatementBody.
    def enterSelectStatementBody(self, ctx:spgdsParser.SelectStatementBodyContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectStatementBody.
    def exitSelectStatementBody(self, ctx:spgdsParser.SelectStatementBodyContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectGraphMatchList.
    def enterSelectGraphMatchList(self, ctx:spgdsParser.SelectGraphMatchListContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectGraphMatchList.
    def exitSelectGraphMatchList(self, ctx:spgdsParser.SelectGraphMatchListContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectGraphMatch.
    def enterSelectGraphMatch(self, ctx:spgdsParser.SelectGraphMatchContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectGraphMatch.
    def exitSelectGraphMatch(self, ctx:spgdsParser.SelectGraphMatchContext):
        pass


    # Enter a parse tree produced by spgdsParser#selectQuerySpecification.
    def enterSelectQuerySpecification(self, ctx:spgdsParser.SelectQuerySpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#selectQuerySpecification.
    def exitSelectQuerySpecification(self, ctx:spgdsParser.SelectQuerySpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#callProcedureStatement.
    def enterCallProcedureStatement(self, ctx:spgdsParser.CallProcedureStatementContext):
        pass

    # Exit a parse tree produced by spgdsParser#callProcedureStatement.
    def exitCallProcedureStatement(self, ctx:spgdsParser.CallProcedureStatementContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureCall.
    def enterProcedureCall(self, ctx:spgdsParser.ProcedureCallContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureCall.
    def exitProcedureCall(self, ctx:spgdsParser.ProcedureCallContext):
        pass


    # Enter a parse tree produced by spgdsParser#inlineProcedureCall.
    def enterInlineProcedureCall(self, ctx:spgdsParser.InlineProcedureCallContext):
        pass

    # Exit a parse tree produced by spgdsParser#inlineProcedureCall.
    def exitInlineProcedureCall(self, ctx:spgdsParser.InlineProcedureCallContext):
        pass


    # Enter a parse tree produced by spgdsParser#variableScopeClause.
    def enterVariableScopeClause(self, ctx:spgdsParser.VariableScopeClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#variableScopeClause.
    def exitVariableScopeClause(self, ctx:spgdsParser.VariableScopeClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingVariableReferenceList.
    def enterBindingVariableReferenceList(self, ctx:spgdsParser.BindingVariableReferenceListContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingVariableReferenceList.
    def exitBindingVariableReferenceList(self, ctx:spgdsParser.BindingVariableReferenceListContext):
        pass


    # Enter a parse tree produced by spgdsParser#namedProcedureCall.
    def enterNamedProcedureCall(self, ctx:spgdsParser.NamedProcedureCallContext):
        pass

    # Exit a parse tree produced by spgdsParser#namedProcedureCall.
    def exitNamedProcedureCall(self, ctx:spgdsParser.NamedProcedureCallContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureArgumentList.
    def enterProcedureArgumentList(self, ctx:spgdsParser.ProcedureArgumentListContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureArgumentList.
    def exitProcedureArgumentList(self, ctx:spgdsParser.ProcedureArgumentListContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureArgument.
    def enterProcedureArgument(self, ctx:spgdsParser.ProcedureArgumentContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureArgument.
    def exitProcedureArgument(self, ctx:spgdsParser.ProcedureArgumentContext):
        pass


    # Enter a parse tree produced by spgdsParser#atSchemaClause.
    def enterAtSchemaClause(self, ctx:spgdsParser.AtSchemaClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#atSchemaClause.
    def exitAtSchemaClause(self, ctx:spgdsParser.AtSchemaClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#useGraphClause.
    def enterUseGraphClause(self, ctx:spgdsParser.UseGraphClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#useGraphClause.
    def exitUseGraphClause(self, ctx:spgdsParser.UseGraphClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPatternBindingTable.
    def enterGraphPatternBindingTable(self, ctx:spgdsParser.GraphPatternBindingTableContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPatternBindingTable.
    def exitGraphPatternBindingTable(self, ctx:spgdsParser.GraphPatternBindingTableContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPatternYieldClause.
    def enterGraphPatternYieldClause(self, ctx:spgdsParser.GraphPatternYieldClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPatternYieldClause.
    def exitGraphPatternYieldClause(self, ctx:spgdsParser.GraphPatternYieldClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPatternYieldItemList.
    def enterGraphPatternYieldItemList(self, ctx:spgdsParser.GraphPatternYieldItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPatternYieldItemList.
    def exitGraphPatternYieldItemList(self, ctx:spgdsParser.GraphPatternYieldItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPatternYieldItem.
    def enterGraphPatternYieldItem(self, ctx:spgdsParser.GraphPatternYieldItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPatternYieldItem.
    def exitGraphPatternYieldItem(self, ctx:spgdsParser.GraphPatternYieldItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPattern.
    def enterGraphPattern(self, ctx:spgdsParser.GraphPatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPattern.
    def exitGraphPattern(self, ctx:spgdsParser.GraphPatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#matchMode.
    def enterMatchMode(self, ctx:spgdsParser.MatchModeContext):
        pass

    # Exit a parse tree produced by spgdsParser#matchMode.
    def exitMatchMode(self, ctx:spgdsParser.MatchModeContext):
        pass


    # Enter a parse tree produced by spgdsParser#repeatableElementsMatchMode.
    def enterRepeatableElementsMatchMode(self, ctx:spgdsParser.RepeatableElementsMatchModeContext):
        pass

    # Exit a parse tree produced by spgdsParser#repeatableElementsMatchMode.
    def exitRepeatableElementsMatchMode(self, ctx:spgdsParser.RepeatableElementsMatchModeContext):
        pass


    # Enter a parse tree produced by spgdsParser#differentEdgesMatchMode.
    def enterDifferentEdgesMatchMode(self, ctx:spgdsParser.DifferentEdgesMatchModeContext):
        pass

    # Exit a parse tree produced by spgdsParser#differentEdgesMatchMode.
    def exitDifferentEdgesMatchMode(self, ctx:spgdsParser.DifferentEdgesMatchModeContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementBindingsOrElements.
    def enterElementBindingsOrElements(self, ctx:spgdsParser.ElementBindingsOrElementsContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementBindingsOrElements.
    def exitElementBindingsOrElements(self, ctx:spgdsParser.ElementBindingsOrElementsContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeBindingsOrEdges.
    def enterEdgeBindingsOrEdges(self, ctx:spgdsParser.EdgeBindingsOrEdgesContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeBindingsOrEdges.
    def exitEdgeBindingsOrEdges(self, ctx:spgdsParser.EdgeBindingsOrEdgesContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathPatternList.
    def enterPathPatternList(self, ctx:spgdsParser.PathPatternListContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathPatternList.
    def exitPathPatternList(self, ctx:spgdsParser.PathPatternListContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathPattern.
    def enterPathPattern(self, ctx:spgdsParser.PathPatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathPattern.
    def exitPathPattern(self, ctx:spgdsParser.PathPatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathVariableDeclaration.
    def enterPathVariableDeclaration(self, ctx:spgdsParser.PathVariableDeclarationContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathVariableDeclaration.
    def exitPathVariableDeclaration(self, ctx:spgdsParser.PathVariableDeclarationContext):
        pass


    # Enter a parse tree produced by spgdsParser#keepClause.
    def enterKeepClause(self, ctx:spgdsParser.KeepClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#keepClause.
    def exitKeepClause(self, ctx:spgdsParser.KeepClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPatternWhereClause.
    def enterGraphPatternWhereClause(self, ctx:spgdsParser.GraphPatternWhereClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPatternWhereClause.
    def exitGraphPatternWhereClause(self, ctx:spgdsParser.GraphPatternWhereClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertGraphPattern.
    def enterInsertGraphPattern(self, ctx:spgdsParser.InsertGraphPatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertGraphPattern.
    def exitInsertGraphPattern(self, ctx:spgdsParser.InsertGraphPatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertPathPatternList.
    def enterInsertPathPatternList(self, ctx:spgdsParser.InsertPathPatternListContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertPathPatternList.
    def exitInsertPathPatternList(self, ctx:spgdsParser.InsertPathPatternListContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertPathPattern.
    def enterInsertPathPattern(self, ctx:spgdsParser.InsertPathPatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertPathPattern.
    def exitInsertPathPattern(self, ctx:spgdsParser.InsertPathPatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertNodePattern.
    def enterInsertNodePattern(self, ctx:spgdsParser.InsertNodePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertNodePattern.
    def exitInsertNodePattern(self, ctx:spgdsParser.InsertNodePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertEdgePattern.
    def enterInsertEdgePattern(self, ctx:spgdsParser.InsertEdgePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertEdgePattern.
    def exitInsertEdgePattern(self, ctx:spgdsParser.InsertEdgePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertEdgePointingLeft.
    def enterInsertEdgePointingLeft(self, ctx:spgdsParser.InsertEdgePointingLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertEdgePointingLeft.
    def exitInsertEdgePointingLeft(self, ctx:spgdsParser.InsertEdgePointingLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertEdgePointingRight.
    def enterInsertEdgePointingRight(self, ctx:spgdsParser.InsertEdgePointingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertEdgePointingRight.
    def exitInsertEdgePointingRight(self, ctx:spgdsParser.InsertEdgePointingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertEdgeUndirected.
    def enterInsertEdgeUndirected(self, ctx:spgdsParser.InsertEdgeUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertEdgeUndirected.
    def exitInsertEdgeUndirected(self, ctx:spgdsParser.InsertEdgeUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#insertElementPatternFiller.
    def enterInsertElementPatternFiller(self, ctx:spgdsParser.InsertElementPatternFillerContext):
        pass

    # Exit a parse tree produced by spgdsParser#insertElementPatternFiller.
    def exitInsertElementPatternFiller(self, ctx:spgdsParser.InsertElementPatternFillerContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelAndPropertySetSpecification.
    def enterLabelAndPropertySetSpecification(self, ctx:spgdsParser.LabelAndPropertySetSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelAndPropertySetSpecification.
    def exitLabelAndPropertySetSpecification(self, ctx:spgdsParser.LabelAndPropertySetSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathPatternPrefix.
    def enterPathPatternPrefix(self, ctx:spgdsParser.PathPatternPrefixContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathPatternPrefix.
    def exitPathPatternPrefix(self, ctx:spgdsParser.PathPatternPrefixContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathModePrefix.
    def enterPathModePrefix(self, ctx:spgdsParser.PathModePrefixContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathModePrefix.
    def exitPathModePrefix(self, ctx:spgdsParser.PathModePrefixContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathMode.
    def enterPathMode(self, ctx:spgdsParser.PathModeContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathMode.
    def exitPathMode(self, ctx:spgdsParser.PathModeContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathSearchPrefix.
    def enterPathSearchPrefix(self, ctx:spgdsParser.PathSearchPrefixContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathSearchPrefix.
    def exitPathSearchPrefix(self, ctx:spgdsParser.PathSearchPrefixContext):
        pass


    # Enter a parse tree produced by spgdsParser#allPathSearch.
    def enterAllPathSearch(self, ctx:spgdsParser.AllPathSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#allPathSearch.
    def exitAllPathSearch(self, ctx:spgdsParser.AllPathSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathOrPaths.
    def enterPathOrPaths(self, ctx:spgdsParser.PathOrPathsContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathOrPaths.
    def exitPathOrPaths(self, ctx:spgdsParser.PathOrPathsContext):
        pass


    # Enter a parse tree produced by spgdsParser#anyPathSearch.
    def enterAnyPathSearch(self, ctx:spgdsParser.AnyPathSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#anyPathSearch.
    def exitAnyPathSearch(self, ctx:spgdsParser.AnyPathSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#numberOfPaths.
    def enterNumberOfPaths(self, ctx:spgdsParser.NumberOfPathsContext):
        pass

    # Exit a parse tree produced by spgdsParser#numberOfPaths.
    def exitNumberOfPaths(self, ctx:spgdsParser.NumberOfPathsContext):
        pass


    # Enter a parse tree produced by spgdsParser#shortestPathSearch.
    def enterShortestPathSearch(self, ctx:spgdsParser.ShortestPathSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#shortestPathSearch.
    def exitShortestPathSearch(self, ctx:spgdsParser.ShortestPathSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#allShortestPathSearch.
    def enterAllShortestPathSearch(self, ctx:spgdsParser.AllShortestPathSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#allShortestPathSearch.
    def exitAllShortestPathSearch(self, ctx:spgdsParser.AllShortestPathSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#anyShortestPathSearch.
    def enterAnyShortestPathSearch(self, ctx:spgdsParser.AnyShortestPathSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#anyShortestPathSearch.
    def exitAnyShortestPathSearch(self, ctx:spgdsParser.AnyShortestPathSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#countedShortestPathSearch.
    def enterCountedShortestPathSearch(self, ctx:spgdsParser.CountedShortestPathSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#countedShortestPathSearch.
    def exitCountedShortestPathSearch(self, ctx:spgdsParser.CountedShortestPathSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#countedShortestGroupSearch.
    def enterCountedShortestGroupSearch(self, ctx:spgdsParser.CountedShortestGroupSearchContext):
        pass

    # Exit a parse tree produced by spgdsParser#countedShortestGroupSearch.
    def exitCountedShortestGroupSearch(self, ctx:spgdsParser.CountedShortestGroupSearchContext):
        pass


    # Enter a parse tree produced by spgdsParser#numberOfGroups.
    def enterNumberOfGroups(self, ctx:spgdsParser.NumberOfGroupsContext):
        pass

    # Exit a parse tree produced by spgdsParser#numberOfGroups.
    def exitNumberOfGroups(self, ctx:spgdsParser.NumberOfGroupsContext):
        pass


    # Enter a parse tree produced by spgdsParser#ppePathTerm.
    def enterPpePathTerm(self, ctx:spgdsParser.PpePathTermContext):
        pass

    # Exit a parse tree produced by spgdsParser#ppePathTerm.
    def exitPpePathTerm(self, ctx:spgdsParser.PpePathTermContext):
        pass


    # Enter a parse tree produced by spgdsParser#ppeMultisetAlternation.
    def enterPpeMultisetAlternation(self, ctx:spgdsParser.PpeMultisetAlternationContext):
        pass

    # Exit a parse tree produced by spgdsParser#ppeMultisetAlternation.
    def exitPpeMultisetAlternation(self, ctx:spgdsParser.PpeMultisetAlternationContext):
        pass


    # Enter a parse tree produced by spgdsParser#ppePatternUnion.
    def enterPpePatternUnion(self, ctx:spgdsParser.PpePatternUnionContext):
        pass

    # Exit a parse tree produced by spgdsParser#ppePatternUnion.
    def exitPpePatternUnion(self, ctx:spgdsParser.PpePatternUnionContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathTerm.
    def enterPathTerm(self, ctx:spgdsParser.PathTermContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathTerm.
    def exitPathTerm(self, ctx:spgdsParser.PathTermContext):
        pass


    # Enter a parse tree produced by spgdsParser#pfPathPrimary.
    def enterPfPathPrimary(self, ctx:spgdsParser.PfPathPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#pfPathPrimary.
    def exitPfPathPrimary(self, ctx:spgdsParser.PfPathPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#pfQuantifiedPathPrimary.
    def enterPfQuantifiedPathPrimary(self, ctx:spgdsParser.PfQuantifiedPathPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#pfQuantifiedPathPrimary.
    def exitPfQuantifiedPathPrimary(self, ctx:spgdsParser.PfQuantifiedPathPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#pfQuestionedPathPrimary.
    def enterPfQuestionedPathPrimary(self, ctx:spgdsParser.PfQuestionedPathPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#pfQuestionedPathPrimary.
    def exitPfQuestionedPathPrimary(self, ctx:spgdsParser.PfQuestionedPathPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#ppElementPattern.
    def enterPpElementPattern(self, ctx:spgdsParser.PpElementPatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#ppElementPattern.
    def exitPpElementPattern(self, ctx:spgdsParser.PpElementPatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#ppParenthesizedPathPatternExpression.
    def enterPpParenthesizedPathPatternExpression(self, ctx:spgdsParser.PpParenthesizedPathPatternExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#ppParenthesizedPathPatternExpression.
    def exitPpParenthesizedPathPatternExpression(self, ctx:spgdsParser.PpParenthesizedPathPatternExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#ppSimplifiedPathPatternExpression.
    def enterPpSimplifiedPathPatternExpression(self, ctx:spgdsParser.PpSimplifiedPathPatternExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#ppSimplifiedPathPatternExpression.
    def exitPpSimplifiedPathPatternExpression(self, ctx:spgdsParser.PpSimplifiedPathPatternExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementPattern.
    def enterElementPattern(self, ctx:spgdsParser.ElementPatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementPattern.
    def exitElementPattern(self, ctx:spgdsParser.ElementPatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodePattern.
    def enterNodePattern(self, ctx:spgdsParser.NodePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodePattern.
    def exitNodePattern(self, ctx:spgdsParser.NodePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementPatternFiller.
    def enterElementPatternFiller(self, ctx:spgdsParser.ElementPatternFillerContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementPatternFiller.
    def exitElementPatternFiller(self, ctx:spgdsParser.ElementPatternFillerContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementVariableDeclaration.
    def enterElementVariableDeclaration(self, ctx:spgdsParser.ElementVariableDeclarationContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementVariableDeclaration.
    def exitElementVariableDeclaration(self, ctx:spgdsParser.ElementVariableDeclarationContext):
        pass


    # Enter a parse tree produced by spgdsParser#isLabelExpression.
    def enterIsLabelExpression(self, ctx:spgdsParser.IsLabelExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#isLabelExpression.
    def exitIsLabelExpression(self, ctx:spgdsParser.IsLabelExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#isOrColon.
    def enterIsOrColon(self, ctx:spgdsParser.IsOrColonContext):
        pass

    # Exit a parse tree produced by spgdsParser#isOrColon.
    def exitIsOrColon(self, ctx:spgdsParser.IsOrColonContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementPatternPredicate.
    def enterElementPatternPredicate(self, ctx:spgdsParser.ElementPatternPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementPatternPredicate.
    def exitElementPatternPredicate(self, ctx:spgdsParser.ElementPatternPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementPatternWhereClause.
    def enterElementPatternWhereClause(self, ctx:spgdsParser.ElementPatternWhereClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementPatternWhereClause.
    def exitElementPatternWhereClause(self, ctx:spgdsParser.ElementPatternWhereClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementPropertySpecification.
    def enterElementPropertySpecification(self, ctx:spgdsParser.ElementPropertySpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementPropertySpecification.
    def exitElementPropertySpecification(self, ctx:spgdsParser.ElementPropertySpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyKeyValuePairList.
    def enterPropertyKeyValuePairList(self, ctx:spgdsParser.PropertyKeyValuePairListContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyKeyValuePairList.
    def exitPropertyKeyValuePairList(self, ctx:spgdsParser.PropertyKeyValuePairListContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyKeyValuePair.
    def enterPropertyKeyValuePair(self, ctx:spgdsParser.PropertyKeyValuePairContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyKeyValuePair.
    def exitPropertyKeyValuePair(self, ctx:spgdsParser.PropertyKeyValuePairContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgePattern.
    def enterEdgePattern(self, ctx:spgdsParser.EdgePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgePattern.
    def exitEdgePattern(self, ctx:spgdsParser.EdgePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgePattern.
    def enterFullEdgePattern(self, ctx:spgdsParser.FullEdgePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgePattern.
    def exitFullEdgePattern(self, ctx:spgdsParser.FullEdgePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgePointingLeft.
    def enterFullEdgePointingLeft(self, ctx:spgdsParser.FullEdgePointingLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgePointingLeft.
    def exitFullEdgePointingLeft(self, ctx:spgdsParser.FullEdgePointingLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgeUndirected.
    def enterFullEdgeUndirected(self, ctx:spgdsParser.FullEdgeUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgeUndirected.
    def exitFullEdgeUndirected(self, ctx:spgdsParser.FullEdgeUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgePointingRight.
    def enterFullEdgePointingRight(self, ctx:spgdsParser.FullEdgePointingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgePointingRight.
    def exitFullEdgePointingRight(self, ctx:spgdsParser.FullEdgePointingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgeLeftOrUndirected.
    def enterFullEdgeLeftOrUndirected(self, ctx:spgdsParser.FullEdgeLeftOrUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgeLeftOrUndirected.
    def exitFullEdgeLeftOrUndirected(self, ctx:spgdsParser.FullEdgeLeftOrUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgeUndirectedOrRight.
    def enterFullEdgeUndirectedOrRight(self, ctx:spgdsParser.FullEdgeUndirectedOrRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgeUndirectedOrRight.
    def exitFullEdgeUndirectedOrRight(self, ctx:spgdsParser.FullEdgeUndirectedOrRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgeLeftOrRight.
    def enterFullEdgeLeftOrRight(self, ctx:spgdsParser.FullEdgeLeftOrRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgeLeftOrRight.
    def exitFullEdgeLeftOrRight(self, ctx:spgdsParser.FullEdgeLeftOrRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#fullEdgeAnyDirection.
    def enterFullEdgeAnyDirection(self, ctx:spgdsParser.FullEdgeAnyDirectionContext):
        pass

    # Exit a parse tree produced by spgdsParser#fullEdgeAnyDirection.
    def exitFullEdgeAnyDirection(self, ctx:spgdsParser.FullEdgeAnyDirectionContext):
        pass


    # Enter a parse tree produced by spgdsParser#abbreviatedEdgePattern.
    def enterAbbreviatedEdgePattern(self, ctx:spgdsParser.AbbreviatedEdgePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#abbreviatedEdgePattern.
    def exitAbbreviatedEdgePattern(self, ctx:spgdsParser.AbbreviatedEdgePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#parenthesizedPathPatternExpression.
    def enterParenthesizedPathPatternExpression(self, ctx:spgdsParser.ParenthesizedPathPatternExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#parenthesizedPathPatternExpression.
    def exitParenthesizedPathPatternExpression(self, ctx:spgdsParser.ParenthesizedPathPatternExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#subpathVariableDeclaration.
    def enterSubpathVariableDeclaration(self, ctx:spgdsParser.SubpathVariableDeclarationContext):
        pass

    # Exit a parse tree produced by spgdsParser#subpathVariableDeclaration.
    def exitSubpathVariableDeclaration(self, ctx:spgdsParser.SubpathVariableDeclarationContext):
        pass


    # Enter a parse tree produced by spgdsParser#parenthesizedPathPatternWhereClause.
    def enterParenthesizedPathPatternWhereClause(self, ctx:spgdsParser.ParenthesizedPathPatternWhereClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#parenthesizedPathPatternWhereClause.
    def exitParenthesizedPathPatternWhereClause(self, ctx:spgdsParser.ParenthesizedPathPatternWhereClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelExpressionNegation.
    def enterLabelExpressionNegation(self, ctx:spgdsParser.LabelExpressionNegationContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelExpressionNegation.
    def exitLabelExpressionNegation(self, ctx:spgdsParser.LabelExpressionNegationContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelExpressionDisjunction.
    def enterLabelExpressionDisjunction(self, ctx:spgdsParser.LabelExpressionDisjunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelExpressionDisjunction.
    def exitLabelExpressionDisjunction(self, ctx:spgdsParser.LabelExpressionDisjunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelExpressionParenthesized.
    def enterLabelExpressionParenthesized(self, ctx:spgdsParser.LabelExpressionParenthesizedContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelExpressionParenthesized.
    def exitLabelExpressionParenthesized(self, ctx:spgdsParser.LabelExpressionParenthesizedContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelExpressionWildcard.
    def enterLabelExpressionWildcard(self, ctx:spgdsParser.LabelExpressionWildcardContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelExpressionWildcard.
    def exitLabelExpressionWildcard(self, ctx:spgdsParser.LabelExpressionWildcardContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelExpressionConjunction.
    def enterLabelExpressionConjunction(self, ctx:spgdsParser.LabelExpressionConjunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelExpressionConjunction.
    def exitLabelExpressionConjunction(self, ctx:spgdsParser.LabelExpressionConjunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelExpressionName.
    def enterLabelExpressionName(self, ctx:spgdsParser.LabelExpressionNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelExpressionName.
    def exitLabelExpressionName(self, ctx:spgdsParser.LabelExpressionNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathVariableReference.
    def enterPathVariableReference(self, ctx:spgdsParser.PathVariableReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathVariableReference.
    def exitPathVariableReference(self, ctx:spgdsParser.PathVariableReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementVariableReference.
    def enterElementVariableReference(self, ctx:spgdsParser.ElementVariableReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementVariableReference.
    def exitElementVariableReference(self, ctx:spgdsParser.ElementVariableReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphPatternQuantifier.
    def enterGraphPatternQuantifier(self, ctx:spgdsParser.GraphPatternQuantifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphPatternQuantifier.
    def exitGraphPatternQuantifier(self, ctx:spgdsParser.GraphPatternQuantifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#fixedQuantifier.
    def enterFixedQuantifier(self, ctx:spgdsParser.FixedQuantifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#fixedQuantifier.
    def exitFixedQuantifier(self, ctx:spgdsParser.FixedQuantifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalQuantifier.
    def enterGeneralQuantifier(self, ctx:spgdsParser.GeneralQuantifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalQuantifier.
    def exitGeneralQuantifier(self, ctx:spgdsParser.GeneralQuantifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#lowerBound.
    def enterLowerBound(self, ctx:spgdsParser.LowerBoundContext):
        pass

    # Exit a parse tree produced by spgdsParser#lowerBound.
    def exitLowerBound(self, ctx:spgdsParser.LowerBoundContext):
        pass


    # Enter a parse tree produced by spgdsParser#upperBound.
    def enterUpperBound(self, ctx:spgdsParser.UpperBoundContext):
        pass

    # Exit a parse tree produced by spgdsParser#upperBound.
    def exitUpperBound(self, ctx:spgdsParser.UpperBoundContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedPathPatternExpression.
    def enterSimplifiedPathPatternExpression(self, ctx:spgdsParser.SimplifiedPathPatternExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedPathPatternExpression.
    def exitSimplifiedPathPatternExpression(self, ctx:spgdsParser.SimplifiedPathPatternExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingLeft.
    def enterSimplifiedDefaultingLeft(self, ctx:spgdsParser.SimplifiedDefaultingLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingLeft.
    def exitSimplifiedDefaultingLeft(self, ctx:spgdsParser.SimplifiedDefaultingLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingUndirected.
    def enterSimplifiedDefaultingUndirected(self, ctx:spgdsParser.SimplifiedDefaultingUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingUndirected.
    def exitSimplifiedDefaultingUndirected(self, ctx:spgdsParser.SimplifiedDefaultingUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingRight.
    def enterSimplifiedDefaultingRight(self, ctx:spgdsParser.SimplifiedDefaultingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingRight.
    def exitSimplifiedDefaultingRight(self, ctx:spgdsParser.SimplifiedDefaultingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingLeftOrUndirected.
    def enterSimplifiedDefaultingLeftOrUndirected(self, ctx:spgdsParser.SimplifiedDefaultingLeftOrUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingLeftOrUndirected.
    def exitSimplifiedDefaultingLeftOrUndirected(self, ctx:spgdsParser.SimplifiedDefaultingLeftOrUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingUndirectedOrRight.
    def enterSimplifiedDefaultingUndirectedOrRight(self, ctx:spgdsParser.SimplifiedDefaultingUndirectedOrRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingUndirectedOrRight.
    def exitSimplifiedDefaultingUndirectedOrRight(self, ctx:spgdsParser.SimplifiedDefaultingUndirectedOrRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingLeftOrRight.
    def enterSimplifiedDefaultingLeftOrRight(self, ctx:spgdsParser.SimplifiedDefaultingLeftOrRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingLeftOrRight.
    def exitSimplifiedDefaultingLeftOrRight(self, ctx:spgdsParser.SimplifiedDefaultingLeftOrRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDefaultingAnyDirection.
    def enterSimplifiedDefaultingAnyDirection(self, ctx:spgdsParser.SimplifiedDefaultingAnyDirectionContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDefaultingAnyDirection.
    def exitSimplifiedDefaultingAnyDirection(self, ctx:spgdsParser.SimplifiedDefaultingAnyDirectionContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedContents.
    def enterSimplifiedContents(self, ctx:spgdsParser.SimplifiedContentsContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedContents.
    def exitSimplifiedContents(self, ctx:spgdsParser.SimplifiedContentsContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedPathUnion.
    def enterSimplifiedPathUnion(self, ctx:spgdsParser.SimplifiedPathUnionContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedPathUnion.
    def exitSimplifiedPathUnion(self, ctx:spgdsParser.SimplifiedPathUnionContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedMultisetAlternation.
    def enterSimplifiedMultisetAlternation(self, ctx:spgdsParser.SimplifiedMultisetAlternationContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedMultisetAlternation.
    def exitSimplifiedMultisetAlternation(self, ctx:spgdsParser.SimplifiedMultisetAlternationContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedFactorLowLabel.
    def enterSimplifiedFactorLowLabel(self, ctx:spgdsParser.SimplifiedFactorLowLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedFactorLowLabel.
    def exitSimplifiedFactorLowLabel(self, ctx:spgdsParser.SimplifiedFactorLowLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedConcatenationLabel.
    def enterSimplifiedConcatenationLabel(self, ctx:spgdsParser.SimplifiedConcatenationLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedConcatenationLabel.
    def exitSimplifiedConcatenationLabel(self, ctx:spgdsParser.SimplifiedConcatenationLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedConjunctionLabel.
    def enterSimplifiedConjunctionLabel(self, ctx:spgdsParser.SimplifiedConjunctionLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedConjunctionLabel.
    def exitSimplifiedConjunctionLabel(self, ctx:spgdsParser.SimplifiedConjunctionLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedFactorHighLabel.
    def enterSimplifiedFactorHighLabel(self, ctx:spgdsParser.SimplifiedFactorHighLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedFactorHighLabel.
    def exitSimplifiedFactorHighLabel(self, ctx:spgdsParser.SimplifiedFactorHighLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedFactorHigh.
    def enterSimplifiedFactorHigh(self, ctx:spgdsParser.SimplifiedFactorHighContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedFactorHigh.
    def exitSimplifiedFactorHigh(self, ctx:spgdsParser.SimplifiedFactorHighContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedQuantified.
    def enterSimplifiedQuantified(self, ctx:spgdsParser.SimplifiedQuantifiedContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedQuantified.
    def exitSimplifiedQuantified(self, ctx:spgdsParser.SimplifiedQuantifiedContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedQuestioned.
    def enterSimplifiedQuestioned(self, ctx:spgdsParser.SimplifiedQuestionedContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedQuestioned.
    def exitSimplifiedQuestioned(self, ctx:spgdsParser.SimplifiedQuestionedContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedTertiary.
    def enterSimplifiedTertiary(self, ctx:spgdsParser.SimplifiedTertiaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedTertiary.
    def exitSimplifiedTertiary(self, ctx:spgdsParser.SimplifiedTertiaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedDirectionOverride.
    def enterSimplifiedDirectionOverride(self, ctx:spgdsParser.SimplifiedDirectionOverrideContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedDirectionOverride.
    def exitSimplifiedDirectionOverride(self, ctx:spgdsParser.SimplifiedDirectionOverrideContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideLeft.
    def enterSimplifiedOverrideLeft(self, ctx:spgdsParser.SimplifiedOverrideLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideLeft.
    def exitSimplifiedOverrideLeft(self, ctx:spgdsParser.SimplifiedOverrideLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideUndirected.
    def enterSimplifiedOverrideUndirected(self, ctx:spgdsParser.SimplifiedOverrideUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideUndirected.
    def exitSimplifiedOverrideUndirected(self, ctx:spgdsParser.SimplifiedOverrideUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideRight.
    def enterSimplifiedOverrideRight(self, ctx:spgdsParser.SimplifiedOverrideRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideRight.
    def exitSimplifiedOverrideRight(self, ctx:spgdsParser.SimplifiedOverrideRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideLeftOrUndirected.
    def enterSimplifiedOverrideLeftOrUndirected(self, ctx:spgdsParser.SimplifiedOverrideLeftOrUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideLeftOrUndirected.
    def exitSimplifiedOverrideLeftOrUndirected(self, ctx:spgdsParser.SimplifiedOverrideLeftOrUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideUndirectedOrRight.
    def enterSimplifiedOverrideUndirectedOrRight(self, ctx:spgdsParser.SimplifiedOverrideUndirectedOrRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideUndirectedOrRight.
    def exitSimplifiedOverrideUndirectedOrRight(self, ctx:spgdsParser.SimplifiedOverrideUndirectedOrRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideLeftOrRight.
    def enterSimplifiedOverrideLeftOrRight(self, ctx:spgdsParser.SimplifiedOverrideLeftOrRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideLeftOrRight.
    def exitSimplifiedOverrideLeftOrRight(self, ctx:spgdsParser.SimplifiedOverrideLeftOrRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedOverrideAnyDirection.
    def enterSimplifiedOverrideAnyDirection(self, ctx:spgdsParser.SimplifiedOverrideAnyDirectionContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedOverrideAnyDirection.
    def exitSimplifiedOverrideAnyDirection(self, ctx:spgdsParser.SimplifiedOverrideAnyDirectionContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedSecondary.
    def enterSimplifiedSecondary(self, ctx:spgdsParser.SimplifiedSecondaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedSecondary.
    def exitSimplifiedSecondary(self, ctx:spgdsParser.SimplifiedSecondaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedNegation.
    def enterSimplifiedNegation(self, ctx:spgdsParser.SimplifiedNegationContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedNegation.
    def exitSimplifiedNegation(self, ctx:spgdsParser.SimplifiedNegationContext):
        pass


    # Enter a parse tree produced by spgdsParser#simplifiedPrimary.
    def enterSimplifiedPrimary(self, ctx:spgdsParser.SimplifiedPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#simplifiedPrimary.
    def exitSimplifiedPrimary(self, ctx:spgdsParser.SimplifiedPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#whereClause.
    def enterWhereClause(self, ctx:spgdsParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#whereClause.
    def exitWhereClause(self, ctx:spgdsParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#yieldClause.
    def enterYieldClause(self, ctx:spgdsParser.YieldClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#yieldClause.
    def exitYieldClause(self, ctx:spgdsParser.YieldClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#yieldItemList.
    def enterYieldItemList(self, ctx:spgdsParser.YieldItemListContext):
        pass

    # Exit a parse tree produced by spgdsParser#yieldItemList.
    def exitYieldItemList(self, ctx:spgdsParser.YieldItemListContext):
        pass


    # Enter a parse tree produced by spgdsParser#yieldItem.
    def enterYieldItem(self, ctx:spgdsParser.YieldItemContext):
        pass

    # Exit a parse tree produced by spgdsParser#yieldItem.
    def exitYieldItem(self, ctx:spgdsParser.YieldItemContext):
        pass


    # Enter a parse tree produced by spgdsParser#yieldItemName.
    def enterYieldItemName(self, ctx:spgdsParser.YieldItemNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#yieldItemName.
    def exitYieldItemName(self, ctx:spgdsParser.YieldItemNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#yieldItemAlias.
    def enterYieldItemAlias(self, ctx:spgdsParser.YieldItemAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#yieldItemAlias.
    def exitYieldItemAlias(self, ctx:spgdsParser.YieldItemAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#groupByClause.
    def enterGroupByClause(self, ctx:spgdsParser.GroupByClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#groupByClause.
    def exitGroupByClause(self, ctx:spgdsParser.GroupByClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#groupingElementList.
    def enterGroupingElementList(self, ctx:spgdsParser.GroupingElementListContext):
        pass

    # Exit a parse tree produced by spgdsParser#groupingElementList.
    def exitGroupingElementList(self, ctx:spgdsParser.GroupingElementListContext):
        pass


    # Enter a parse tree produced by spgdsParser#groupingElement.
    def enterGroupingElement(self, ctx:spgdsParser.GroupingElementContext):
        pass

    # Exit a parse tree produced by spgdsParser#groupingElement.
    def exitGroupingElement(self, ctx:spgdsParser.GroupingElementContext):
        pass


    # Enter a parse tree produced by spgdsParser#emptyGroupingSet.
    def enterEmptyGroupingSet(self, ctx:spgdsParser.EmptyGroupingSetContext):
        pass

    # Exit a parse tree produced by spgdsParser#emptyGroupingSet.
    def exitEmptyGroupingSet(self, ctx:spgdsParser.EmptyGroupingSetContext):
        pass


    # Enter a parse tree produced by spgdsParser#orderByClause.
    def enterOrderByClause(self, ctx:spgdsParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#orderByClause.
    def exitOrderByClause(self, ctx:spgdsParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#sortSpecificationList.
    def enterSortSpecificationList(self, ctx:spgdsParser.SortSpecificationListContext):
        pass

    # Exit a parse tree produced by spgdsParser#sortSpecificationList.
    def exitSortSpecificationList(self, ctx:spgdsParser.SortSpecificationListContext):
        pass


    # Enter a parse tree produced by spgdsParser#sortSpecification.
    def enterSortSpecification(self, ctx:spgdsParser.SortSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#sortSpecification.
    def exitSortSpecification(self, ctx:spgdsParser.SortSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#sortKey.
    def enterSortKey(self, ctx:spgdsParser.SortKeyContext):
        pass

    # Exit a parse tree produced by spgdsParser#sortKey.
    def exitSortKey(self, ctx:spgdsParser.SortKeyContext):
        pass


    # Enter a parse tree produced by spgdsParser#orderingSpecification.
    def enterOrderingSpecification(self, ctx:spgdsParser.OrderingSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#orderingSpecification.
    def exitOrderingSpecification(self, ctx:spgdsParser.OrderingSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nullOrdering.
    def enterNullOrdering(self, ctx:spgdsParser.NullOrderingContext):
        pass

    # Exit a parse tree produced by spgdsParser#nullOrdering.
    def exitNullOrdering(self, ctx:spgdsParser.NullOrderingContext):
        pass


    # Enter a parse tree produced by spgdsParser#limitClause.
    def enterLimitClause(self, ctx:spgdsParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#limitClause.
    def exitLimitClause(self, ctx:spgdsParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#offsetClause.
    def enterOffsetClause(self, ctx:spgdsParser.OffsetClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#offsetClause.
    def exitOffsetClause(self, ctx:spgdsParser.OffsetClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#offsetSynonym.
    def enterOffsetSynonym(self, ctx:spgdsParser.OffsetSynonymContext):
        pass

    # Exit a parse tree produced by spgdsParser#offsetSynonym.
    def exitOffsetSynonym(self, ctx:spgdsParser.OffsetSynonymContext):
        pass


    # Enter a parse tree produced by spgdsParser#schemaReference.
    def enterSchemaReference(self, ctx:spgdsParser.SchemaReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#schemaReference.
    def exitSchemaReference(self, ctx:spgdsParser.SchemaReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#absoluteCatalogSchemaReference.
    def enterAbsoluteCatalogSchemaReference(self, ctx:spgdsParser.AbsoluteCatalogSchemaReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#absoluteCatalogSchemaReference.
    def exitAbsoluteCatalogSchemaReference(self, ctx:spgdsParser.AbsoluteCatalogSchemaReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#catalogSchemaParentAndName.
    def enterCatalogSchemaParentAndName(self, ctx:spgdsParser.CatalogSchemaParentAndNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#catalogSchemaParentAndName.
    def exitCatalogSchemaParentAndName(self, ctx:spgdsParser.CatalogSchemaParentAndNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#relativeCatalogSchemaReference.
    def enterRelativeCatalogSchemaReference(self, ctx:spgdsParser.RelativeCatalogSchemaReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#relativeCatalogSchemaReference.
    def exitRelativeCatalogSchemaReference(self, ctx:spgdsParser.RelativeCatalogSchemaReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#predefinedSchemaReference.
    def enterPredefinedSchemaReference(self, ctx:spgdsParser.PredefinedSchemaReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#predefinedSchemaReference.
    def exitPredefinedSchemaReference(self, ctx:spgdsParser.PredefinedSchemaReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#absoluteDirectoryPath.
    def enterAbsoluteDirectoryPath(self, ctx:spgdsParser.AbsoluteDirectoryPathContext):
        pass

    # Exit a parse tree produced by spgdsParser#absoluteDirectoryPath.
    def exitAbsoluteDirectoryPath(self, ctx:spgdsParser.AbsoluteDirectoryPathContext):
        pass


    # Enter a parse tree produced by spgdsParser#relativeDirectoryPath.
    def enterRelativeDirectoryPath(self, ctx:spgdsParser.RelativeDirectoryPathContext):
        pass

    # Exit a parse tree produced by spgdsParser#relativeDirectoryPath.
    def exitRelativeDirectoryPath(self, ctx:spgdsParser.RelativeDirectoryPathContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleDirectoryPath.
    def enterSimpleDirectoryPath(self, ctx:spgdsParser.SimpleDirectoryPathContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleDirectoryPath.
    def exitSimpleDirectoryPath(self, ctx:spgdsParser.SimpleDirectoryPathContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphReference.
    def enterGraphReference(self, ctx:spgdsParser.GraphReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphReference.
    def exitGraphReference(self, ctx:spgdsParser.GraphReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#catalogGraphParentAndName.
    def enterCatalogGraphParentAndName(self, ctx:spgdsParser.CatalogGraphParentAndNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#catalogGraphParentAndName.
    def exitCatalogGraphParentAndName(self, ctx:spgdsParser.CatalogGraphParentAndNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#homeGraph.
    def enterHomeGraph(self, ctx:spgdsParser.HomeGraphContext):
        pass

    # Exit a parse tree produced by spgdsParser#homeGraph.
    def exitHomeGraph(self, ctx:spgdsParser.HomeGraphContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphTypeReference.
    def enterGraphTypeReference(self, ctx:spgdsParser.GraphTypeReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphTypeReference.
    def exitGraphTypeReference(self, ctx:spgdsParser.GraphTypeReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#catalogGraphTypeParentAndName.
    def enterCatalogGraphTypeParentAndName(self, ctx:spgdsParser.CatalogGraphTypeParentAndNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#catalogGraphTypeParentAndName.
    def exitCatalogGraphTypeParentAndName(self, ctx:spgdsParser.CatalogGraphTypeParentAndNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableReference.
    def enterBindingTableReference(self, ctx:spgdsParser.BindingTableReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableReference.
    def exitBindingTableReference(self, ctx:spgdsParser.BindingTableReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureReference.
    def enterProcedureReference(self, ctx:spgdsParser.ProcedureReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureReference.
    def exitProcedureReference(self, ctx:spgdsParser.ProcedureReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#catalogProcedureParentAndName.
    def enterCatalogProcedureParentAndName(self, ctx:spgdsParser.CatalogProcedureParentAndNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#catalogProcedureParentAndName.
    def exitCatalogProcedureParentAndName(self, ctx:spgdsParser.CatalogProcedureParentAndNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#catalogObjectParentReference.
    def enterCatalogObjectParentReference(self, ctx:spgdsParser.CatalogObjectParentReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#catalogObjectParentReference.
    def exitCatalogObjectParentReference(self, ctx:spgdsParser.CatalogObjectParentReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#referenceParameterSpecification.
    def enterReferenceParameterSpecification(self, ctx:spgdsParser.ReferenceParameterSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#referenceParameterSpecification.
    def exitReferenceParameterSpecification(self, ctx:spgdsParser.ReferenceParameterSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nestedGraphTypeSpecification.
    def enterNestedGraphTypeSpecification(self, ctx:spgdsParser.NestedGraphTypeSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nestedGraphTypeSpecification.
    def exitNestedGraphTypeSpecification(self, ctx:spgdsParser.NestedGraphTypeSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphTypeSpecificationBody.
    def enterGraphTypeSpecificationBody(self, ctx:spgdsParser.GraphTypeSpecificationBodyContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphTypeSpecificationBody.
    def exitGraphTypeSpecificationBody(self, ctx:spgdsParser.GraphTypeSpecificationBodyContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementTypeList.
    def enterElementTypeList(self, ctx:spgdsParser.ElementTypeListContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementTypeList.
    def exitElementTypeList(self, ctx:spgdsParser.ElementTypeListContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementTypeSpecification.
    def enterElementTypeSpecification(self, ctx:spgdsParser.ElementTypeSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementTypeSpecification.
    def exitElementTypeSpecification(self, ctx:spgdsParser.ElementTypeSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypeSpecification.
    def enterNodeTypeSpecification(self, ctx:spgdsParser.NodeTypeSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypeSpecification.
    def exitNodeTypeSpecification(self, ctx:spgdsParser.NodeTypeSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypePattern.
    def enterNodeTypePattern(self, ctx:spgdsParser.NodeTypePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypePattern.
    def exitNodeTypePattern(self, ctx:spgdsParser.NodeTypePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypePhrase.
    def enterNodeTypePhrase(self, ctx:spgdsParser.NodeTypePhraseContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypePhrase.
    def exitNodeTypePhrase(self, ctx:spgdsParser.NodeTypePhraseContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypePhraseFiller.
    def enterNodeTypePhraseFiller(self, ctx:spgdsParser.NodeTypePhraseFillerContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypePhraseFiller.
    def exitNodeTypePhraseFiller(self, ctx:spgdsParser.NodeTypePhraseFillerContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypeFiller.
    def enterNodeTypeFiller(self, ctx:spgdsParser.NodeTypeFillerContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypeFiller.
    def exitNodeTypeFiller(self, ctx:spgdsParser.NodeTypeFillerContext):
        pass


    # Enter a parse tree produced by spgdsParser#localNodeTypeAlias.
    def enterLocalNodeTypeAlias(self, ctx:spgdsParser.LocalNodeTypeAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#localNodeTypeAlias.
    def exitLocalNodeTypeAlias(self, ctx:spgdsParser.LocalNodeTypeAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypeImpliedContent.
    def enterNodeTypeImpliedContent(self, ctx:spgdsParser.NodeTypeImpliedContentContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypeImpliedContent.
    def exitNodeTypeImpliedContent(self, ctx:spgdsParser.NodeTypeImpliedContentContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypeKeyLabelSet.
    def enterNodeTypeKeyLabelSet(self, ctx:spgdsParser.NodeTypeKeyLabelSetContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypeKeyLabelSet.
    def exitNodeTypeKeyLabelSet(self, ctx:spgdsParser.NodeTypeKeyLabelSetContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypeLabelSet.
    def enterNodeTypeLabelSet(self, ctx:spgdsParser.NodeTypeLabelSetContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypeLabelSet.
    def exitNodeTypeLabelSet(self, ctx:spgdsParser.NodeTypeLabelSetContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypePropertyTypes.
    def enterNodeTypePropertyTypes(self, ctx:spgdsParser.NodeTypePropertyTypesContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypePropertyTypes.
    def exitNodeTypePropertyTypes(self, ctx:spgdsParser.NodeTypePropertyTypesContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypeSpecification.
    def enterEdgeTypeSpecification(self, ctx:spgdsParser.EdgeTypeSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypeSpecification.
    def exitEdgeTypeSpecification(self, ctx:spgdsParser.EdgeTypeSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePattern.
    def enterEdgeTypePattern(self, ctx:spgdsParser.EdgeTypePatternContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePattern.
    def exitEdgeTypePattern(self, ctx:spgdsParser.EdgeTypePatternContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePhrase.
    def enterEdgeTypePhrase(self, ctx:spgdsParser.EdgeTypePhraseContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePhrase.
    def exitEdgeTypePhrase(self, ctx:spgdsParser.EdgeTypePhraseContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePhraseFiller.
    def enterEdgeTypePhraseFiller(self, ctx:spgdsParser.EdgeTypePhraseFillerContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePhraseFiller.
    def exitEdgeTypePhraseFiller(self, ctx:spgdsParser.EdgeTypePhraseFillerContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypeFiller.
    def enterEdgeTypeFiller(self, ctx:spgdsParser.EdgeTypeFillerContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypeFiller.
    def exitEdgeTypeFiller(self, ctx:spgdsParser.EdgeTypeFillerContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypeImpliedContent.
    def enterEdgeTypeImpliedContent(self, ctx:spgdsParser.EdgeTypeImpliedContentContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypeImpliedContent.
    def exitEdgeTypeImpliedContent(self, ctx:spgdsParser.EdgeTypeImpliedContentContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypeKeyLabelSet.
    def enterEdgeTypeKeyLabelSet(self, ctx:spgdsParser.EdgeTypeKeyLabelSetContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypeKeyLabelSet.
    def exitEdgeTypeKeyLabelSet(self, ctx:spgdsParser.EdgeTypeKeyLabelSetContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypeLabelSet.
    def enterEdgeTypeLabelSet(self, ctx:spgdsParser.EdgeTypeLabelSetContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypeLabelSet.
    def exitEdgeTypeLabelSet(self, ctx:spgdsParser.EdgeTypeLabelSetContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePropertyTypes.
    def enterEdgeTypePropertyTypes(self, ctx:spgdsParser.EdgeTypePropertyTypesContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePropertyTypes.
    def exitEdgeTypePropertyTypes(self, ctx:spgdsParser.EdgeTypePropertyTypesContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePatternDirected.
    def enterEdgeTypePatternDirected(self, ctx:spgdsParser.EdgeTypePatternDirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePatternDirected.
    def exitEdgeTypePatternDirected(self, ctx:spgdsParser.EdgeTypePatternDirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePatternPointingRight.
    def enterEdgeTypePatternPointingRight(self, ctx:spgdsParser.EdgeTypePatternPointingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePatternPointingRight.
    def exitEdgeTypePatternPointingRight(self, ctx:spgdsParser.EdgeTypePatternPointingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePatternPointingLeft.
    def enterEdgeTypePatternPointingLeft(self, ctx:spgdsParser.EdgeTypePatternPointingLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePatternPointingLeft.
    def exitEdgeTypePatternPointingLeft(self, ctx:spgdsParser.EdgeTypePatternPointingLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypePatternUndirected.
    def enterEdgeTypePatternUndirected(self, ctx:spgdsParser.EdgeTypePatternUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypePatternUndirected.
    def exitEdgeTypePatternUndirected(self, ctx:spgdsParser.EdgeTypePatternUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#arcTypePointingRight.
    def enterArcTypePointingRight(self, ctx:spgdsParser.ArcTypePointingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#arcTypePointingRight.
    def exitArcTypePointingRight(self, ctx:spgdsParser.ArcTypePointingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#arcTypePointingLeft.
    def enterArcTypePointingLeft(self, ctx:spgdsParser.ArcTypePointingLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#arcTypePointingLeft.
    def exitArcTypePointingLeft(self, ctx:spgdsParser.ArcTypePointingLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#arcTypeUndirected.
    def enterArcTypeUndirected(self, ctx:spgdsParser.ArcTypeUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#arcTypeUndirected.
    def exitArcTypeUndirected(self, ctx:spgdsParser.ArcTypeUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#sourceNodeTypeReference.
    def enterSourceNodeTypeReference(self, ctx:spgdsParser.SourceNodeTypeReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#sourceNodeTypeReference.
    def exitSourceNodeTypeReference(self, ctx:spgdsParser.SourceNodeTypeReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#destinationNodeTypeReference.
    def enterDestinationNodeTypeReference(self, ctx:spgdsParser.DestinationNodeTypeReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#destinationNodeTypeReference.
    def exitDestinationNodeTypeReference(self, ctx:spgdsParser.DestinationNodeTypeReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeKind.
    def enterEdgeKind(self, ctx:spgdsParser.EdgeKindContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeKind.
    def exitEdgeKind(self, ctx:spgdsParser.EdgeKindContext):
        pass


    # Enter a parse tree produced by spgdsParser#endpointPairPhrase.
    def enterEndpointPairPhrase(self, ctx:spgdsParser.EndpointPairPhraseContext):
        pass

    # Exit a parse tree produced by spgdsParser#endpointPairPhrase.
    def exitEndpointPairPhrase(self, ctx:spgdsParser.EndpointPairPhraseContext):
        pass


    # Enter a parse tree produced by spgdsParser#endpointPair.
    def enterEndpointPair(self, ctx:spgdsParser.EndpointPairContext):
        pass

    # Exit a parse tree produced by spgdsParser#endpointPair.
    def exitEndpointPair(self, ctx:spgdsParser.EndpointPairContext):
        pass


    # Enter a parse tree produced by spgdsParser#endpointPairDirected.
    def enterEndpointPairDirected(self, ctx:spgdsParser.EndpointPairDirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#endpointPairDirected.
    def exitEndpointPairDirected(self, ctx:spgdsParser.EndpointPairDirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#endpointPairPointingRight.
    def enterEndpointPairPointingRight(self, ctx:spgdsParser.EndpointPairPointingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#endpointPairPointingRight.
    def exitEndpointPairPointingRight(self, ctx:spgdsParser.EndpointPairPointingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#endpointPairPointingLeft.
    def enterEndpointPairPointingLeft(self, ctx:spgdsParser.EndpointPairPointingLeftContext):
        pass

    # Exit a parse tree produced by spgdsParser#endpointPairPointingLeft.
    def exitEndpointPairPointingLeft(self, ctx:spgdsParser.EndpointPairPointingLeftContext):
        pass


    # Enter a parse tree produced by spgdsParser#endpointPairUndirected.
    def enterEndpointPairUndirected(self, ctx:spgdsParser.EndpointPairUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#endpointPairUndirected.
    def exitEndpointPairUndirected(self, ctx:spgdsParser.EndpointPairUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#connectorPointingRight.
    def enterConnectorPointingRight(self, ctx:spgdsParser.ConnectorPointingRightContext):
        pass

    # Exit a parse tree produced by spgdsParser#connectorPointingRight.
    def exitConnectorPointingRight(self, ctx:spgdsParser.ConnectorPointingRightContext):
        pass


    # Enter a parse tree produced by spgdsParser#connectorUndirected.
    def enterConnectorUndirected(self, ctx:spgdsParser.ConnectorUndirectedContext):
        pass

    # Exit a parse tree produced by spgdsParser#connectorUndirected.
    def exitConnectorUndirected(self, ctx:spgdsParser.ConnectorUndirectedContext):
        pass


    # Enter a parse tree produced by spgdsParser#sourceNodeTypeAlias.
    def enterSourceNodeTypeAlias(self, ctx:spgdsParser.SourceNodeTypeAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#sourceNodeTypeAlias.
    def exitSourceNodeTypeAlias(self, ctx:spgdsParser.SourceNodeTypeAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#destinationNodeTypeAlias.
    def enterDestinationNodeTypeAlias(self, ctx:spgdsParser.DestinationNodeTypeAliasContext):
        pass

    # Exit a parse tree produced by spgdsParser#destinationNodeTypeAlias.
    def exitDestinationNodeTypeAlias(self, ctx:spgdsParser.DestinationNodeTypeAliasContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelSetPhrase.
    def enterLabelSetPhrase(self, ctx:spgdsParser.LabelSetPhraseContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelSetPhrase.
    def exitLabelSetPhrase(self, ctx:spgdsParser.LabelSetPhraseContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelSetSpecification.
    def enterLabelSetSpecification(self, ctx:spgdsParser.LabelSetSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelSetSpecification.
    def exitLabelSetSpecification(self, ctx:spgdsParser.LabelSetSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyTypesSpecification.
    def enterPropertyTypesSpecification(self, ctx:spgdsParser.PropertyTypesSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyTypesSpecification.
    def exitPropertyTypesSpecification(self, ctx:spgdsParser.PropertyTypesSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyTypeList.
    def enterPropertyTypeList(self, ctx:spgdsParser.PropertyTypeListContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyTypeList.
    def exitPropertyTypeList(self, ctx:spgdsParser.PropertyTypeListContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyType.
    def enterPropertyType(self, ctx:spgdsParser.PropertyTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyType.
    def exitPropertyType(self, ctx:spgdsParser.PropertyTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyValueType.
    def enterPropertyValueType(self, ctx:spgdsParser.PropertyValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyValueType.
    def exitPropertyValueType(self, ctx:spgdsParser.PropertyValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableType.
    def enterBindingTableType(self, ctx:spgdsParser.BindingTableTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableType.
    def exitBindingTableType(self, ctx:spgdsParser.BindingTableTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#dynamicPropertyValueTypeLabel.
    def enterDynamicPropertyValueTypeLabel(self, ctx:spgdsParser.DynamicPropertyValueTypeLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#dynamicPropertyValueTypeLabel.
    def exitDynamicPropertyValueTypeLabel(self, ctx:spgdsParser.DynamicPropertyValueTypeLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#closedDynamicUnionTypeAtl1.
    def enterClosedDynamicUnionTypeAtl1(self, ctx:spgdsParser.ClosedDynamicUnionTypeAtl1Context):
        pass

    # Exit a parse tree produced by spgdsParser#closedDynamicUnionTypeAtl1.
    def exitClosedDynamicUnionTypeAtl1(self, ctx:spgdsParser.ClosedDynamicUnionTypeAtl1Context):
        pass


    # Enter a parse tree produced by spgdsParser#closedDynamicUnionTypeAtl2.
    def enterClosedDynamicUnionTypeAtl2(self, ctx:spgdsParser.ClosedDynamicUnionTypeAtl2Context):
        pass

    # Exit a parse tree produced by spgdsParser#closedDynamicUnionTypeAtl2.
    def exitClosedDynamicUnionTypeAtl2(self, ctx:spgdsParser.ClosedDynamicUnionTypeAtl2Context):
        pass


    # Enter a parse tree produced by spgdsParser#pathValueTypeLabel.
    def enterPathValueTypeLabel(self, ctx:spgdsParser.PathValueTypeLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathValueTypeLabel.
    def exitPathValueTypeLabel(self, ctx:spgdsParser.PathValueTypeLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueTypeAlt3.
    def enterListValueTypeAlt3(self, ctx:spgdsParser.ListValueTypeAlt3Context):
        pass

    # Exit a parse tree produced by spgdsParser#listValueTypeAlt3.
    def exitListValueTypeAlt3(self, ctx:spgdsParser.ListValueTypeAlt3Context):
        pass


    # Enter a parse tree produced by spgdsParser#listValueTypeAlt2.
    def enterListValueTypeAlt2(self, ctx:spgdsParser.ListValueTypeAlt2Context):
        pass

    # Exit a parse tree produced by spgdsParser#listValueTypeAlt2.
    def exitListValueTypeAlt2(self, ctx:spgdsParser.ListValueTypeAlt2Context):
        pass


    # Enter a parse tree produced by spgdsParser#listValueTypeAlt1.
    def enterListValueTypeAlt1(self, ctx:spgdsParser.ListValueTypeAlt1Context):
        pass

    # Exit a parse tree produced by spgdsParser#listValueTypeAlt1.
    def exitListValueTypeAlt1(self, ctx:spgdsParser.ListValueTypeAlt1Context):
        pass


    # Enter a parse tree produced by spgdsParser#predefinedTypeLabel.
    def enterPredefinedTypeLabel(self, ctx:spgdsParser.PredefinedTypeLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#predefinedTypeLabel.
    def exitPredefinedTypeLabel(self, ctx:spgdsParser.PredefinedTypeLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#recordTypeLabel.
    def enterRecordTypeLabel(self, ctx:spgdsParser.RecordTypeLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#recordTypeLabel.
    def exitRecordTypeLabel(self, ctx:spgdsParser.RecordTypeLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#openDynamicUnionTypeLabel.
    def enterOpenDynamicUnionTypeLabel(self, ctx:spgdsParser.OpenDynamicUnionTypeLabelContext):
        pass

    # Exit a parse tree produced by spgdsParser#openDynamicUnionTypeLabel.
    def exitOpenDynamicUnionTypeLabel(self, ctx:spgdsParser.OpenDynamicUnionTypeLabelContext):
        pass


    # Enter a parse tree produced by spgdsParser#typed.
    def enterTyped(self, ctx:spgdsParser.TypedContext):
        pass

    # Exit a parse tree produced by spgdsParser#typed.
    def exitTyped(self, ctx:spgdsParser.TypedContext):
        pass


    # Enter a parse tree produced by spgdsParser#predefinedType.
    def enterPredefinedType(self, ctx:spgdsParser.PredefinedTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#predefinedType.
    def exitPredefinedType(self, ctx:spgdsParser.PredefinedTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#booleanType.
    def enterBooleanType(self, ctx:spgdsParser.BooleanTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#booleanType.
    def exitBooleanType(self, ctx:spgdsParser.BooleanTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#characterStringType.
    def enterCharacterStringType(self, ctx:spgdsParser.CharacterStringTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#characterStringType.
    def exitCharacterStringType(self, ctx:spgdsParser.CharacterStringTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#byteStringType.
    def enterByteStringType(self, ctx:spgdsParser.ByteStringTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#byteStringType.
    def exitByteStringType(self, ctx:spgdsParser.ByteStringTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#minLength.
    def enterMinLength(self, ctx:spgdsParser.MinLengthContext):
        pass

    # Exit a parse tree produced by spgdsParser#minLength.
    def exitMinLength(self, ctx:spgdsParser.MinLengthContext):
        pass


    # Enter a parse tree produced by spgdsParser#maxLength.
    def enterMaxLength(self, ctx:spgdsParser.MaxLengthContext):
        pass

    # Exit a parse tree produced by spgdsParser#maxLength.
    def exitMaxLength(self, ctx:spgdsParser.MaxLengthContext):
        pass


    # Enter a parse tree produced by spgdsParser#fixedLength.
    def enterFixedLength(self, ctx:spgdsParser.FixedLengthContext):
        pass

    # Exit a parse tree produced by spgdsParser#fixedLength.
    def exitFixedLength(self, ctx:spgdsParser.FixedLengthContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericType.
    def enterNumericType(self, ctx:spgdsParser.NumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericType.
    def exitNumericType(self, ctx:spgdsParser.NumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#exactNumericType.
    def enterExactNumericType(self, ctx:spgdsParser.ExactNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#exactNumericType.
    def exitExactNumericType(self, ctx:spgdsParser.ExactNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#binaryExactNumericType.
    def enterBinaryExactNumericType(self, ctx:spgdsParser.BinaryExactNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#binaryExactNumericType.
    def exitBinaryExactNumericType(self, ctx:spgdsParser.BinaryExactNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#signedBinaryExactNumericType.
    def enterSignedBinaryExactNumericType(self, ctx:spgdsParser.SignedBinaryExactNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#signedBinaryExactNumericType.
    def exitSignedBinaryExactNumericType(self, ctx:spgdsParser.SignedBinaryExactNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#unsignedBinaryExactNumericType.
    def enterUnsignedBinaryExactNumericType(self, ctx:spgdsParser.UnsignedBinaryExactNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#unsignedBinaryExactNumericType.
    def exitUnsignedBinaryExactNumericType(self, ctx:spgdsParser.UnsignedBinaryExactNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#verboseBinaryExactNumericType.
    def enterVerboseBinaryExactNumericType(self, ctx:spgdsParser.VerboseBinaryExactNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#verboseBinaryExactNumericType.
    def exitVerboseBinaryExactNumericType(self, ctx:spgdsParser.VerboseBinaryExactNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#decimalExactNumericType.
    def enterDecimalExactNumericType(self, ctx:spgdsParser.DecimalExactNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#decimalExactNumericType.
    def exitDecimalExactNumericType(self, ctx:spgdsParser.DecimalExactNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#precision.
    def enterPrecision(self, ctx:spgdsParser.PrecisionContext):
        pass

    # Exit a parse tree produced by spgdsParser#precision.
    def exitPrecision(self, ctx:spgdsParser.PrecisionContext):
        pass


    # Enter a parse tree produced by spgdsParser#scale.
    def enterScale(self, ctx:spgdsParser.ScaleContext):
        pass

    # Exit a parse tree produced by spgdsParser#scale.
    def exitScale(self, ctx:spgdsParser.ScaleContext):
        pass


    # Enter a parse tree produced by spgdsParser#approximateNumericType.
    def enterApproximateNumericType(self, ctx:spgdsParser.ApproximateNumericTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#approximateNumericType.
    def exitApproximateNumericType(self, ctx:spgdsParser.ApproximateNumericTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#temporalType.
    def enterTemporalType(self, ctx:spgdsParser.TemporalTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#temporalType.
    def exitTemporalType(self, ctx:spgdsParser.TemporalTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#temporalInstantType.
    def enterTemporalInstantType(self, ctx:spgdsParser.TemporalInstantTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#temporalInstantType.
    def exitTemporalInstantType(self, ctx:spgdsParser.TemporalInstantTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeType.
    def enterDatetimeType(self, ctx:spgdsParser.DatetimeTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeType.
    def exitDatetimeType(self, ctx:spgdsParser.DatetimeTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#localdatetimeType.
    def enterLocaldatetimeType(self, ctx:spgdsParser.LocaldatetimeTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#localdatetimeType.
    def exitLocaldatetimeType(self, ctx:spgdsParser.LocaldatetimeTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#dateType.
    def enterDateType(self, ctx:spgdsParser.DateTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#dateType.
    def exitDateType(self, ctx:spgdsParser.DateTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#timeType.
    def enterTimeType(self, ctx:spgdsParser.TimeTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#timeType.
    def exitTimeType(self, ctx:spgdsParser.TimeTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#localtimeType.
    def enterLocaltimeType(self, ctx:spgdsParser.LocaltimeTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#localtimeType.
    def exitLocaltimeType(self, ctx:spgdsParser.LocaltimeTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#temporalDurationType.
    def enterTemporalDurationType(self, ctx:spgdsParser.TemporalDurationTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#temporalDurationType.
    def exitTemporalDurationType(self, ctx:spgdsParser.TemporalDurationTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#temporalDurationQualifier.
    def enterTemporalDurationQualifier(self, ctx:spgdsParser.TemporalDurationQualifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#temporalDurationQualifier.
    def exitTemporalDurationQualifier(self, ctx:spgdsParser.TemporalDurationQualifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#referenceValueType.
    def enterReferenceValueType(self, ctx:spgdsParser.ReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#referenceValueType.
    def exitReferenceValueType(self, ctx:spgdsParser.ReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#immaterialValueType.
    def enterImmaterialValueType(self, ctx:spgdsParser.ImmaterialValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#immaterialValueType.
    def exitImmaterialValueType(self, ctx:spgdsParser.ImmaterialValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#nullType.
    def enterNullType(self, ctx:spgdsParser.NullTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#nullType.
    def exitNullType(self, ctx:spgdsParser.NullTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#emptyType.
    def enterEmptyType(self, ctx:spgdsParser.EmptyTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#emptyType.
    def exitEmptyType(self, ctx:spgdsParser.EmptyTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphReferenceValueType.
    def enterGraphReferenceValueType(self, ctx:spgdsParser.GraphReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphReferenceValueType.
    def exitGraphReferenceValueType(self, ctx:spgdsParser.GraphReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#closedGraphReferenceValueType.
    def enterClosedGraphReferenceValueType(self, ctx:spgdsParser.ClosedGraphReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#closedGraphReferenceValueType.
    def exitClosedGraphReferenceValueType(self, ctx:spgdsParser.ClosedGraphReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#openGraphReferenceValueType.
    def enterOpenGraphReferenceValueType(self, ctx:spgdsParser.OpenGraphReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#openGraphReferenceValueType.
    def exitOpenGraphReferenceValueType(self, ctx:spgdsParser.OpenGraphReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableReferenceValueType.
    def enterBindingTableReferenceValueType(self, ctx:spgdsParser.BindingTableReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableReferenceValueType.
    def exitBindingTableReferenceValueType(self, ctx:spgdsParser.BindingTableReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeReferenceValueType.
    def enterNodeReferenceValueType(self, ctx:spgdsParser.NodeReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeReferenceValueType.
    def exitNodeReferenceValueType(self, ctx:spgdsParser.NodeReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#closedNodeReferenceValueType.
    def enterClosedNodeReferenceValueType(self, ctx:spgdsParser.ClosedNodeReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#closedNodeReferenceValueType.
    def exitClosedNodeReferenceValueType(self, ctx:spgdsParser.ClosedNodeReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#openNodeReferenceValueType.
    def enterOpenNodeReferenceValueType(self, ctx:spgdsParser.OpenNodeReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#openNodeReferenceValueType.
    def exitOpenNodeReferenceValueType(self, ctx:spgdsParser.OpenNodeReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeReferenceValueType.
    def enterEdgeReferenceValueType(self, ctx:spgdsParser.EdgeReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeReferenceValueType.
    def exitEdgeReferenceValueType(self, ctx:spgdsParser.EdgeReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#closedEdgeReferenceValueType.
    def enterClosedEdgeReferenceValueType(self, ctx:spgdsParser.ClosedEdgeReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#closedEdgeReferenceValueType.
    def exitClosedEdgeReferenceValueType(self, ctx:spgdsParser.ClosedEdgeReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#openEdgeReferenceValueType.
    def enterOpenEdgeReferenceValueType(self, ctx:spgdsParser.OpenEdgeReferenceValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#openEdgeReferenceValueType.
    def exitOpenEdgeReferenceValueType(self, ctx:spgdsParser.OpenEdgeReferenceValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathValueType.
    def enterPathValueType(self, ctx:spgdsParser.PathValueTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathValueType.
    def exitPathValueType(self, ctx:spgdsParser.PathValueTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueTypeName.
    def enterListValueTypeName(self, ctx:spgdsParser.ListValueTypeNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#listValueTypeName.
    def exitListValueTypeName(self, ctx:spgdsParser.ListValueTypeNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueTypeNameSynonym.
    def enterListValueTypeNameSynonym(self, ctx:spgdsParser.ListValueTypeNameSynonymContext):
        pass

    # Exit a parse tree produced by spgdsParser#listValueTypeNameSynonym.
    def exitListValueTypeNameSynonym(self, ctx:spgdsParser.ListValueTypeNameSynonymContext):
        pass


    # Enter a parse tree produced by spgdsParser#recordType.
    def enterRecordType(self, ctx:spgdsParser.RecordTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#recordType.
    def exitRecordType(self, ctx:spgdsParser.RecordTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#fieldTypesSpecification.
    def enterFieldTypesSpecification(self, ctx:spgdsParser.FieldTypesSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#fieldTypesSpecification.
    def exitFieldTypesSpecification(self, ctx:spgdsParser.FieldTypesSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#fieldTypeList.
    def enterFieldTypeList(self, ctx:spgdsParser.FieldTypeListContext):
        pass

    # Exit a parse tree produced by spgdsParser#fieldTypeList.
    def exitFieldTypeList(self, ctx:spgdsParser.FieldTypeListContext):
        pass


    # Enter a parse tree produced by spgdsParser#notNull.
    def enterNotNull(self, ctx:spgdsParser.NotNullContext):
        pass

    # Exit a parse tree produced by spgdsParser#notNull.
    def exitNotNull(self, ctx:spgdsParser.NotNullContext):
        pass


    # Enter a parse tree produced by spgdsParser#fieldType.
    def enterFieldType(self, ctx:spgdsParser.FieldTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#fieldType.
    def exitFieldType(self, ctx:spgdsParser.FieldTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#searchCondition.
    def enterSearchCondition(self, ctx:spgdsParser.SearchConditionContext):
        pass

    # Exit a parse tree produced by spgdsParser#searchCondition.
    def exitSearchCondition(self, ctx:spgdsParser.SearchConditionContext):
        pass


    # Enter a parse tree produced by spgdsParser#predicate.
    def enterPredicate(self, ctx:spgdsParser.PredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#predicate.
    def exitPredicate(self, ctx:spgdsParser.PredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#compOp.
    def enterCompOp(self, ctx:spgdsParser.CompOpContext):
        pass

    # Exit a parse tree produced by spgdsParser#compOp.
    def exitCompOp(self, ctx:spgdsParser.CompOpContext):
        pass


    # Enter a parse tree produced by spgdsParser#existsPredicate.
    def enterExistsPredicate(self, ctx:spgdsParser.ExistsPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#existsPredicate.
    def exitExistsPredicate(self, ctx:spgdsParser.ExistsPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#nullPredicate.
    def enterNullPredicate(self, ctx:spgdsParser.NullPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#nullPredicate.
    def exitNullPredicate(self, ctx:spgdsParser.NullPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#nullPredicatePart2.
    def enterNullPredicatePart2(self, ctx:spgdsParser.NullPredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#nullPredicatePart2.
    def exitNullPredicatePart2(self, ctx:spgdsParser.NullPredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#valueTypePredicate.
    def enterValueTypePredicate(self, ctx:spgdsParser.ValueTypePredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueTypePredicate.
    def exitValueTypePredicate(self, ctx:spgdsParser.ValueTypePredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueTypePredicatePart2.
    def enterValueTypePredicatePart2(self, ctx:spgdsParser.ValueTypePredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#valueTypePredicatePart2.
    def exitValueTypePredicatePart2(self, ctx:spgdsParser.ValueTypePredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#normalizedPredicatePart2.
    def enterNormalizedPredicatePart2(self, ctx:spgdsParser.NormalizedPredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#normalizedPredicatePart2.
    def exitNormalizedPredicatePart2(self, ctx:spgdsParser.NormalizedPredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#directedPredicate.
    def enterDirectedPredicate(self, ctx:spgdsParser.DirectedPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#directedPredicate.
    def exitDirectedPredicate(self, ctx:spgdsParser.DirectedPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#directedPredicatePart2.
    def enterDirectedPredicatePart2(self, ctx:spgdsParser.DirectedPredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#directedPredicatePart2.
    def exitDirectedPredicatePart2(self, ctx:spgdsParser.DirectedPredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#labeledPredicate.
    def enterLabeledPredicate(self, ctx:spgdsParser.LabeledPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#labeledPredicate.
    def exitLabeledPredicate(self, ctx:spgdsParser.LabeledPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#labeledPredicatePart2.
    def enterLabeledPredicatePart2(self, ctx:spgdsParser.LabeledPredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#labeledPredicatePart2.
    def exitLabeledPredicatePart2(self, ctx:spgdsParser.LabeledPredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#isLabeledOrColon.
    def enterIsLabeledOrColon(self, ctx:spgdsParser.IsLabeledOrColonContext):
        pass

    # Exit a parse tree produced by spgdsParser#isLabeledOrColon.
    def exitIsLabeledOrColon(self, ctx:spgdsParser.IsLabeledOrColonContext):
        pass


    # Enter a parse tree produced by spgdsParser#sourceDestinationPredicate.
    def enterSourceDestinationPredicate(self, ctx:spgdsParser.SourceDestinationPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#sourceDestinationPredicate.
    def exitSourceDestinationPredicate(self, ctx:spgdsParser.SourceDestinationPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeReference.
    def enterNodeReference(self, ctx:spgdsParser.NodeReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeReference.
    def exitNodeReference(self, ctx:spgdsParser.NodeReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#sourcePredicatePart2.
    def enterSourcePredicatePart2(self, ctx:spgdsParser.SourcePredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#sourcePredicatePart2.
    def exitSourcePredicatePart2(self, ctx:spgdsParser.SourcePredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#destinationPredicatePart2.
    def enterDestinationPredicatePart2(self, ctx:spgdsParser.DestinationPredicatePart2Context):
        pass

    # Exit a parse tree produced by spgdsParser#destinationPredicatePart2.
    def exitDestinationPredicatePart2(self, ctx:spgdsParser.DestinationPredicatePart2Context):
        pass


    # Enter a parse tree produced by spgdsParser#edgeReference.
    def enterEdgeReference(self, ctx:spgdsParser.EdgeReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeReference.
    def exitEdgeReference(self, ctx:spgdsParser.EdgeReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#all_differentPredicate.
    def enterAll_differentPredicate(self, ctx:spgdsParser.All_differentPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#all_differentPredicate.
    def exitAll_differentPredicate(self, ctx:spgdsParser.All_differentPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#samePredicate.
    def enterSamePredicate(self, ctx:spgdsParser.SamePredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#samePredicate.
    def exitSamePredicate(self, ctx:spgdsParser.SamePredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#property_existsPredicate.
    def enterProperty_existsPredicate(self, ctx:spgdsParser.Property_existsPredicateContext):
        pass

    # Exit a parse tree produced by spgdsParser#property_existsPredicate.
    def exitProperty_existsPredicate(self, ctx:spgdsParser.Property_existsPredicateContext):
        pass


    # Enter a parse tree produced by spgdsParser#conjunctiveExprAlt.
    def enterConjunctiveExprAlt(self, ctx:spgdsParser.ConjunctiveExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#conjunctiveExprAlt.
    def exitConjunctiveExprAlt(self, ctx:spgdsParser.ConjunctiveExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyGraphExprAlt.
    def enterPropertyGraphExprAlt(self, ctx:spgdsParser.PropertyGraphExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyGraphExprAlt.
    def exitPropertyGraphExprAlt(self, ctx:spgdsParser.PropertyGraphExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#multDivExprAlt.
    def enterMultDivExprAlt(self, ctx:spgdsParser.MultDivExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#multDivExprAlt.
    def exitMultDivExprAlt(self, ctx:spgdsParser.MultDivExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableExprAlt.
    def enterBindingTableExprAlt(self, ctx:spgdsParser.BindingTableExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableExprAlt.
    def exitBindingTableExprAlt(self, ctx:spgdsParser.BindingTableExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#signedExprAlt.
    def enterSignedExprAlt(self, ctx:spgdsParser.SignedExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#signedExprAlt.
    def exitSignedExprAlt(self, ctx:spgdsParser.SignedExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#isNotExprAlt.
    def enterIsNotExprAlt(self, ctx:spgdsParser.IsNotExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#isNotExprAlt.
    def exitIsNotExprAlt(self, ctx:spgdsParser.IsNotExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#normalizedPredicateExprAlt.
    def enterNormalizedPredicateExprAlt(self, ctx:spgdsParser.NormalizedPredicateExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#normalizedPredicateExprAlt.
    def exitNormalizedPredicateExprAlt(self, ctx:spgdsParser.NormalizedPredicateExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#notExprAlt.
    def enterNotExprAlt(self, ctx:spgdsParser.NotExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#notExprAlt.
    def exitNotExprAlt(self, ctx:spgdsParser.NotExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueFunctionExprAlt.
    def enterValueFunctionExprAlt(self, ctx:spgdsParser.ValueFunctionExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueFunctionExprAlt.
    def exitValueFunctionExprAlt(self, ctx:spgdsParser.ValueFunctionExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#concatenationExprAlt.
    def enterConcatenationExprAlt(self, ctx:spgdsParser.ConcatenationExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#concatenationExprAlt.
    def exitConcatenationExprAlt(self, ctx:spgdsParser.ConcatenationExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#disjunctiveExprAlt.
    def enterDisjunctiveExprAlt(self, ctx:spgdsParser.DisjunctiveExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#disjunctiveExprAlt.
    def exitDisjunctiveExprAlt(self, ctx:spgdsParser.DisjunctiveExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#comparisonExprAlt.
    def enterComparisonExprAlt(self, ctx:spgdsParser.ComparisonExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#comparisonExprAlt.
    def exitComparisonExprAlt(self, ctx:spgdsParser.ComparisonExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#primaryExprAlt.
    def enterPrimaryExprAlt(self, ctx:spgdsParser.PrimaryExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#primaryExprAlt.
    def exitPrimaryExprAlt(self, ctx:spgdsParser.PrimaryExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#addSubtractExprAlt.
    def enterAddSubtractExprAlt(self, ctx:spgdsParser.AddSubtractExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#addSubtractExprAlt.
    def exitAddSubtractExprAlt(self, ctx:spgdsParser.AddSubtractExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#predicateExprAlt.
    def enterPredicateExprAlt(self, ctx:spgdsParser.PredicateExprAltContext):
        pass

    # Exit a parse tree produced by spgdsParser#predicateExprAlt.
    def exitPredicateExprAlt(self, ctx:spgdsParser.PredicateExprAltContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueFunction.
    def enterValueFunction(self, ctx:spgdsParser.ValueFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueFunction.
    def exitValueFunction(self, ctx:spgdsParser.ValueFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#booleanValueExpression.
    def enterBooleanValueExpression(self, ctx:spgdsParser.BooleanValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#booleanValueExpression.
    def exitBooleanValueExpression(self, ctx:spgdsParser.BooleanValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#characterOrByteStringFunction.
    def enterCharacterOrByteStringFunction(self, ctx:spgdsParser.CharacterOrByteStringFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#characterOrByteStringFunction.
    def exitCharacterOrByteStringFunction(self, ctx:spgdsParser.CharacterOrByteStringFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#subCharacterOrByteString.
    def enterSubCharacterOrByteString(self, ctx:spgdsParser.SubCharacterOrByteStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#subCharacterOrByteString.
    def exitSubCharacterOrByteString(self, ctx:spgdsParser.SubCharacterOrByteStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimSingleCharacterOrByteString.
    def enterTrimSingleCharacterOrByteString(self, ctx:spgdsParser.TrimSingleCharacterOrByteStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimSingleCharacterOrByteString.
    def exitTrimSingleCharacterOrByteString(self, ctx:spgdsParser.TrimSingleCharacterOrByteStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#foldCharacterString.
    def enterFoldCharacterString(self, ctx:spgdsParser.FoldCharacterStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#foldCharacterString.
    def exitFoldCharacterString(self, ctx:spgdsParser.FoldCharacterStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimMultiCharacterCharacterString.
    def enterTrimMultiCharacterCharacterString(self, ctx:spgdsParser.TrimMultiCharacterCharacterStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimMultiCharacterCharacterString.
    def exitTrimMultiCharacterCharacterString(self, ctx:spgdsParser.TrimMultiCharacterCharacterStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#normalizeCharacterString.
    def enterNormalizeCharacterString(self, ctx:spgdsParser.NormalizeCharacterStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#normalizeCharacterString.
    def exitNormalizeCharacterString(self, ctx:spgdsParser.NormalizeCharacterStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeReferenceValueExpression.
    def enterNodeReferenceValueExpression(self, ctx:spgdsParser.NodeReferenceValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeReferenceValueExpression.
    def exitNodeReferenceValueExpression(self, ctx:spgdsParser.NodeReferenceValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeReferenceValueExpression.
    def enterEdgeReferenceValueExpression(self, ctx:spgdsParser.EdgeReferenceValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeReferenceValueExpression.
    def exitEdgeReferenceValueExpression(self, ctx:spgdsParser.EdgeReferenceValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#aggregatingValueExpression.
    def enterAggregatingValueExpression(self, ctx:spgdsParser.AggregatingValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#aggregatingValueExpression.
    def exitAggregatingValueExpression(self, ctx:spgdsParser.AggregatingValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueExpressionPrimary.
    def enterValueExpressionPrimary(self, ctx:spgdsParser.ValueExpressionPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueExpressionPrimary.
    def exitValueExpressionPrimary(self, ctx:spgdsParser.ValueExpressionPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#parenthesizedValueExpression.
    def enterParenthesizedValueExpression(self, ctx:spgdsParser.ParenthesizedValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#parenthesizedValueExpression.
    def exitParenthesizedValueExpression(self, ctx:spgdsParser.ParenthesizedValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#nonParenthesizedValueExpressionPrimary.
    def enterNonParenthesizedValueExpressionPrimary(self, ctx:spgdsParser.NonParenthesizedValueExpressionPrimaryContext):
        pass

    # Exit a parse tree produced by spgdsParser#nonParenthesizedValueExpressionPrimary.
    def exitNonParenthesizedValueExpressionPrimary(self, ctx:spgdsParser.NonParenthesizedValueExpressionPrimaryContext):
        pass


    # Enter a parse tree produced by spgdsParser#nonParenthesizedValueExpressionPrimarySpecialCase.
    def enterNonParenthesizedValueExpressionPrimarySpecialCase(self, ctx:spgdsParser.NonParenthesizedValueExpressionPrimarySpecialCaseContext):
        pass

    # Exit a parse tree produced by spgdsParser#nonParenthesizedValueExpressionPrimarySpecialCase.
    def exitNonParenthesizedValueExpressionPrimarySpecialCase(self, ctx:spgdsParser.NonParenthesizedValueExpressionPrimarySpecialCaseContext):
        pass


    # Enter a parse tree produced by spgdsParser#unsignedValueSpecification.
    def enterUnsignedValueSpecification(self, ctx:spgdsParser.UnsignedValueSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#unsignedValueSpecification.
    def exitUnsignedValueSpecification(self, ctx:spgdsParser.UnsignedValueSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#nonNegativeIntegerSpecification.
    def enterNonNegativeIntegerSpecification(self, ctx:spgdsParser.NonNegativeIntegerSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#nonNegativeIntegerSpecification.
    def exitNonNegativeIntegerSpecification(self, ctx:spgdsParser.NonNegativeIntegerSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalValueSpecification.
    def enterGeneralValueSpecification(self, ctx:spgdsParser.GeneralValueSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalValueSpecification.
    def exitGeneralValueSpecification(self, ctx:spgdsParser.GeneralValueSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#dynamicParameterSpecification.
    def enterDynamicParameterSpecification(self, ctx:spgdsParser.DynamicParameterSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#dynamicParameterSpecification.
    def exitDynamicParameterSpecification(self, ctx:spgdsParser.DynamicParameterSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#letValueExpression.
    def enterLetValueExpression(self, ctx:spgdsParser.LetValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#letValueExpression.
    def exitLetValueExpression(self, ctx:spgdsParser.LetValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#valueQueryExpression.
    def enterValueQueryExpression(self, ctx:spgdsParser.ValueQueryExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#valueQueryExpression.
    def exitValueQueryExpression(self, ctx:spgdsParser.ValueQueryExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#caseExpression.
    def enterCaseExpression(self, ctx:spgdsParser.CaseExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#caseExpression.
    def exitCaseExpression(self, ctx:spgdsParser.CaseExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#caseAbbreviation.
    def enterCaseAbbreviation(self, ctx:spgdsParser.CaseAbbreviationContext):
        pass

    # Exit a parse tree produced by spgdsParser#caseAbbreviation.
    def exitCaseAbbreviation(self, ctx:spgdsParser.CaseAbbreviationContext):
        pass


    # Enter a parse tree produced by spgdsParser#caseSpecification.
    def enterCaseSpecification(self, ctx:spgdsParser.CaseSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#caseSpecification.
    def exitCaseSpecification(self, ctx:spgdsParser.CaseSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleCase.
    def enterSimpleCase(self, ctx:spgdsParser.SimpleCaseContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleCase.
    def exitSimpleCase(self, ctx:spgdsParser.SimpleCaseContext):
        pass


    # Enter a parse tree produced by spgdsParser#searchedCase.
    def enterSearchedCase(self, ctx:spgdsParser.SearchedCaseContext):
        pass

    # Exit a parse tree produced by spgdsParser#searchedCase.
    def exitSearchedCase(self, ctx:spgdsParser.SearchedCaseContext):
        pass


    # Enter a parse tree produced by spgdsParser#simpleWhenClause.
    def enterSimpleWhenClause(self, ctx:spgdsParser.SimpleWhenClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#simpleWhenClause.
    def exitSimpleWhenClause(self, ctx:spgdsParser.SimpleWhenClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#searchedWhenClause.
    def enterSearchedWhenClause(self, ctx:spgdsParser.SearchedWhenClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#searchedWhenClause.
    def exitSearchedWhenClause(self, ctx:spgdsParser.SearchedWhenClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#elseClause.
    def enterElseClause(self, ctx:spgdsParser.ElseClauseContext):
        pass

    # Exit a parse tree produced by spgdsParser#elseClause.
    def exitElseClause(self, ctx:spgdsParser.ElseClauseContext):
        pass


    # Enter a parse tree produced by spgdsParser#caseOperand.
    def enterCaseOperand(self, ctx:spgdsParser.CaseOperandContext):
        pass

    # Exit a parse tree produced by spgdsParser#caseOperand.
    def exitCaseOperand(self, ctx:spgdsParser.CaseOperandContext):
        pass


    # Enter a parse tree produced by spgdsParser#whenOperandList.
    def enterWhenOperandList(self, ctx:spgdsParser.WhenOperandListContext):
        pass

    # Exit a parse tree produced by spgdsParser#whenOperandList.
    def exitWhenOperandList(self, ctx:spgdsParser.WhenOperandListContext):
        pass


    # Enter a parse tree produced by spgdsParser#whenOperand.
    def enterWhenOperand(self, ctx:spgdsParser.WhenOperandContext):
        pass

    # Exit a parse tree produced by spgdsParser#whenOperand.
    def exitWhenOperand(self, ctx:spgdsParser.WhenOperandContext):
        pass


    # Enter a parse tree produced by spgdsParser#result.
    def enterResult(self, ctx:spgdsParser.ResultContext):
        pass

    # Exit a parse tree produced by spgdsParser#result.
    def exitResult(self, ctx:spgdsParser.ResultContext):
        pass


    # Enter a parse tree produced by spgdsParser#resultExpression.
    def enterResultExpression(self, ctx:spgdsParser.ResultExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#resultExpression.
    def exitResultExpression(self, ctx:spgdsParser.ResultExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#castSpecification.
    def enterCastSpecification(self, ctx:spgdsParser.CastSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#castSpecification.
    def exitCastSpecification(self, ctx:spgdsParser.CastSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#castOperand.
    def enterCastOperand(self, ctx:spgdsParser.CastOperandContext):
        pass

    # Exit a parse tree produced by spgdsParser#castOperand.
    def exitCastOperand(self, ctx:spgdsParser.CastOperandContext):
        pass


    # Enter a parse tree produced by spgdsParser#castTarget.
    def enterCastTarget(self, ctx:spgdsParser.CastTargetContext):
        pass

    # Exit a parse tree produced by spgdsParser#castTarget.
    def exitCastTarget(self, ctx:spgdsParser.CastTargetContext):
        pass


    # Enter a parse tree produced by spgdsParser#aggregateFunction.
    def enterAggregateFunction(self, ctx:spgdsParser.AggregateFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#aggregateFunction.
    def exitAggregateFunction(self, ctx:spgdsParser.AggregateFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalSetFunction.
    def enterGeneralSetFunction(self, ctx:spgdsParser.GeneralSetFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalSetFunction.
    def exitGeneralSetFunction(self, ctx:spgdsParser.GeneralSetFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#binarySetFunction.
    def enterBinarySetFunction(self, ctx:spgdsParser.BinarySetFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#binarySetFunction.
    def exitBinarySetFunction(self, ctx:spgdsParser.BinarySetFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalSetFunctionType.
    def enterGeneralSetFunctionType(self, ctx:spgdsParser.GeneralSetFunctionTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalSetFunctionType.
    def exitGeneralSetFunctionType(self, ctx:spgdsParser.GeneralSetFunctionTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#setQuantifier.
    def enterSetQuantifier(self, ctx:spgdsParser.SetQuantifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#setQuantifier.
    def exitSetQuantifier(self, ctx:spgdsParser.SetQuantifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#binarySetFunctionType.
    def enterBinarySetFunctionType(self, ctx:spgdsParser.BinarySetFunctionTypeContext):
        pass

    # Exit a parse tree produced by spgdsParser#binarySetFunctionType.
    def exitBinarySetFunctionType(self, ctx:spgdsParser.BinarySetFunctionTypeContext):
        pass


    # Enter a parse tree produced by spgdsParser#dependentValueExpression.
    def enterDependentValueExpression(self, ctx:spgdsParser.DependentValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#dependentValueExpression.
    def exitDependentValueExpression(self, ctx:spgdsParser.DependentValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#independentValueExpression.
    def enterIndependentValueExpression(self, ctx:spgdsParser.IndependentValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#independentValueExpression.
    def exitIndependentValueExpression(self, ctx:spgdsParser.IndependentValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#element_idFunction.
    def enterElement_idFunction(self, ctx:spgdsParser.Element_idFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#element_idFunction.
    def exitElement_idFunction(self, ctx:spgdsParser.Element_idFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingVariableReference.
    def enterBindingVariableReference(self, ctx:spgdsParser.BindingVariableReferenceContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingVariableReference.
    def exitBindingVariableReference(self, ctx:spgdsParser.BindingVariableReferenceContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathValueExpression.
    def enterPathValueExpression(self, ctx:spgdsParser.PathValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathValueExpression.
    def exitPathValueExpression(self, ctx:spgdsParser.PathValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathValueConstructor.
    def enterPathValueConstructor(self, ctx:spgdsParser.PathValueConstructorContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathValueConstructor.
    def exitPathValueConstructor(self, ctx:spgdsParser.PathValueConstructorContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathValueConstructorByEnumeration.
    def enterPathValueConstructorByEnumeration(self, ctx:spgdsParser.PathValueConstructorByEnumerationContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathValueConstructorByEnumeration.
    def exitPathValueConstructorByEnumeration(self, ctx:spgdsParser.PathValueConstructorByEnumerationContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathElementList.
    def enterPathElementList(self, ctx:spgdsParser.PathElementListContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathElementList.
    def exitPathElementList(self, ctx:spgdsParser.PathElementListContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathElementListStart.
    def enterPathElementListStart(self, ctx:spgdsParser.PathElementListStartContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathElementListStart.
    def exitPathElementListStart(self, ctx:spgdsParser.PathElementListStartContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathElementListStep.
    def enterPathElementListStep(self, ctx:spgdsParser.PathElementListStepContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathElementListStep.
    def exitPathElementListStep(self, ctx:spgdsParser.PathElementListStepContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueExpression.
    def enterListValueExpression(self, ctx:spgdsParser.ListValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#listValueExpression.
    def exitListValueExpression(self, ctx:spgdsParser.ListValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueFunction.
    def enterListValueFunction(self, ctx:spgdsParser.ListValueFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#listValueFunction.
    def exitListValueFunction(self, ctx:spgdsParser.ListValueFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimListFunction.
    def enterTrimListFunction(self, ctx:spgdsParser.TrimListFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimListFunction.
    def exitTrimListFunction(self, ctx:spgdsParser.TrimListFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementsFunction.
    def enterElementsFunction(self, ctx:spgdsParser.ElementsFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementsFunction.
    def exitElementsFunction(self, ctx:spgdsParser.ElementsFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueConstructor.
    def enterListValueConstructor(self, ctx:spgdsParser.ListValueConstructorContext):
        pass

    # Exit a parse tree produced by spgdsParser#listValueConstructor.
    def exitListValueConstructor(self, ctx:spgdsParser.ListValueConstructorContext):
        pass


    # Enter a parse tree produced by spgdsParser#listValueConstructorByEnumeration.
    def enterListValueConstructorByEnumeration(self, ctx:spgdsParser.ListValueConstructorByEnumerationContext):
        pass

    # Exit a parse tree produced by spgdsParser#listValueConstructorByEnumeration.
    def exitListValueConstructorByEnumeration(self, ctx:spgdsParser.ListValueConstructorByEnumerationContext):
        pass


    # Enter a parse tree produced by spgdsParser#listElementList.
    def enterListElementList(self, ctx:spgdsParser.ListElementListContext):
        pass

    # Exit a parse tree produced by spgdsParser#listElementList.
    def exitListElementList(self, ctx:spgdsParser.ListElementListContext):
        pass


    # Enter a parse tree produced by spgdsParser#listElement.
    def enterListElement(self, ctx:spgdsParser.ListElementContext):
        pass

    # Exit a parse tree produced by spgdsParser#listElement.
    def exitListElement(self, ctx:spgdsParser.ListElementContext):
        pass


    # Enter a parse tree produced by spgdsParser#recordConstructor.
    def enterRecordConstructor(self, ctx:spgdsParser.RecordConstructorContext):
        pass

    # Exit a parse tree produced by spgdsParser#recordConstructor.
    def exitRecordConstructor(self, ctx:spgdsParser.RecordConstructorContext):
        pass


    # Enter a parse tree produced by spgdsParser#fieldsSpecification.
    def enterFieldsSpecification(self, ctx:spgdsParser.FieldsSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#fieldsSpecification.
    def exitFieldsSpecification(self, ctx:spgdsParser.FieldsSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#fieldList.
    def enterFieldList(self, ctx:spgdsParser.FieldListContext):
        pass

    # Exit a parse tree produced by spgdsParser#fieldList.
    def exitFieldList(self, ctx:spgdsParser.FieldListContext):
        pass


    # Enter a parse tree produced by spgdsParser#field.
    def enterField(self, ctx:spgdsParser.FieldContext):
        pass

    # Exit a parse tree produced by spgdsParser#field.
    def exitField(self, ctx:spgdsParser.FieldContext):
        pass


    # Enter a parse tree produced by spgdsParser#truthValue.
    def enterTruthValue(self, ctx:spgdsParser.TruthValueContext):
        pass

    # Exit a parse tree produced by spgdsParser#truthValue.
    def exitTruthValue(self, ctx:spgdsParser.TruthValueContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericValueExpression.
    def enterNumericValueExpression(self, ctx:spgdsParser.NumericValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericValueExpression.
    def exitNumericValueExpression(self, ctx:spgdsParser.NumericValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericValueFunction.
    def enterNumericValueFunction(self, ctx:spgdsParser.NumericValueFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericValueFunction.
    def exitNumericValueFunction(self, ctx:spgdsParser.NumericValueFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#lengthExpression.
    def enterLengthExpression(self, ctx:spgdsParser.LengthExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#lengthExpression.
    def exitLengthExpression(self, ctx:spgdsParser.LengthExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#cardinalityExpression.
    def enterCardinalityExpression(self, ctx:spgdsParser.CardinalityExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#cardinalityExpression.
    def exitCardinalityExpression(self, ctx:spgdsParser.CardinalityExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#cardinalityExpressionArgument.
    def enterCardinalityExpressionArgument(self, ctx:spgdsParser.CardinalityExpressionArgumentContext):
        pass

    # Exit a parse tree produced by spgdsParser#cardinalityExpressionArgument.
    def exitCardinalityExpressionArgument(self, ctx:spgdsParser.CardinalityExpressionArgumentContext):
        pass


    # Enter a parse tree produced by spgdsParser#charLengthExpression.
    def enterCharLengthExpression(self, ctx:spgdsParser.CharLengthExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#charLengthExpression.
    def exitCharLengthExpression(self, ctx:spgdsParser.CharLengthExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#byteLengthExpression.
    def enterByteLengthExpression(self, ctx:spgdsParser.ByteLengthExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#byteLengthExpression.
    def exitByteLengthExpression(self, ctx:spgdsParser.ByteLengthExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathLengthExpression.
    def enterPathLengthExpression(self, ctx:spgdsParser.PathLengthExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathLengthExpression.
    def exitPathLengthExpression(self, ctx:spgdsParser.PathLengthExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#absoluteValueExpression.
    def enterAbsoluteValueExpression(self, ctx:spgdsParser.AbsoluteValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#absoluteValueExpression.
    def exitAbsoluteValueExpression(self, ctx:spgdsParser.AbsoluteValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#modulusExpression.
    def enterModulusExpression(self, ctx:spgdsParser.ModulusExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#modulusExpression.
    def exitModulusExpression(self, ctx:spgdsParser.ModulusExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericValueExpressionDividend.
    def enterNumericValueExpressionDividend(self, ctx:spgdsParser.NumericValueExpressionDividendContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericValueExpressionDividend.
    def exitNumericValueExpressionDividend(self, ctx:spgdsParser.NumericValueExpressionDividendContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericValueExpressionDivisor.
    def enterNumericValueExpressionDivisor(self, ctx:spgdsParser.NumericValueExpressionDivisorContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericValueExpressionDivisor.
    def exitNumericValueExpressionDivisor(self, ctx:spgdsParser.NumericValueExpressionDivisorContext):
        pass


    # Enter a parse tree produced by spgdsParser#trigonometricFunction.
    def enterTrigonometricFunction(self, ctx:spgdsParser.TrigonometricFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#trigonometricFunction.
    def exitTrigonometricFunction(self, ctx:spgdsParser.TrigonometricFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#trigonometricFunctionName.
    def enterTrigonometricFunctionName(self, ctx:spgdsParser.TrigonometricFunctionNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#trigonometricFunctionName.
    def exitTrigonometricFunctionName(self, ctx:spgdsParser.TrigonometricFunctionNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalLogarithmFunction.
    def enterGeneralLogarithmFunction(self, ctx:spgdsParser.GeneralLogarithmFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalLogarithmFunction.
    def exitGeneralLogarithmFunction(self, ctx:spgdsParser.GeneralLogarithmFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalLogarithmBase.
    def enterGeneralLogarithmBase(self, ctx:spgdsParser.GeneralLogarithmBaseContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalLogarithmBase.
    def exitGeneralLogarithmBase(self, ctx:spgdsParser.GeneralLogarithmBaseContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalLogarithmArgument.
    def enterGeneralLogarithmArgument(self, ctx:spgdsParser.GeneralLogarithmArgumentContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalLogarithmArgument.
    def exitGeneralLogarithmArgument(self, ctx:spgdsParser.GeneralLogarithmArgumentContext):
        pass


    # Enter a parse tree produced by spgdsParser#commonLogarithm.
    def enterCommonLogarithm(self, ctx:spgdsParser.CommonLogarithmContext):
        pass

    # Exit a parse tree produced by spgdsParser#commonLogarithm.
    def exitCommonLogarithm(self, ctx:spgdsParser.CommonLogarithmContext):
        pass


    # Enter a parse tree produced by spgdsParser#naturalLogarithm.
    def enterNaturalLogarithm(self, ctx:spgdsParser.NaturalLogarithmContext):
        pass

    # Exit a parse tree produced by spgdsParser#naturalLogarithm.
    def exitNaturalLogarithm(self, ctx:spgdsParser.NaturalLogarithmContext):
        pass


    # Enter a parse tree produced by spgdsParser#exponentialFunction.
    def enterExponentialFunction(self, ctx:spgdsParser.ExponentialFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#exponentialFunction.
    def exitExponentialFunction(self, ctx:spgdsParser.ExponentialFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#powerFunction.
    def enterPowerFunction(self, ctx:spgdsParser.PowerFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#powerFunction.
    def exitPowerFunction(self, ctx:spgdsParser.PowerFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericValueExpressionBase.
    def enterNumericValueExpressionBase(self, ctx:spgdsParser.NumericValueExpressionBaseContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericValueExpressionBase.
    def exitNumericValueExpressionBase(self, ctx:spgdsParser.NumericValueExpressionBaseContext):
        pass


    # Enter a parse tree produced by spgdsParser#numericValueExpressionExponent.
    def enterNumericValueExpressionExponent(self, ctx:spgdsParser.NumericValueExpressionExponentContext):
        pass

    # Exit a parse tree produced by spgdsParser#numericValueExpressionExponent.
    def exitNumericValueExpressionExponent(self, ctx:spgdsParser.NumericValueExpressionExponentContext):
        pass


    # Enter a parse tree produced by spgdsParser#squareRoot.
    def enterSquareRoot(self, ctx:spgdsParser.SquareRootContext):
        pass

    # Exit a parse tree produced by spgdsParser#squareRoot.
    def exitSquareRoot(self, ctx:spgdsParser.SquareRootContext):
        pass


    # Enter a parse tree produced by spgdsParser#floorFunction.
    def enterFloorFunction(self, ctx:spgdsParser.FloorFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#floorFunction.
    def exitFloorFunction(self, ctx:spgdsParser.FloorFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#ceilingFunction.
    def enterCeilingFunction(self, ctx:spgdsParser.CeilingFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#ceilingFunction.
    def exitCeilingFunction(self, ctx:spgdsParser.CeilingFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#characterStringValueExpression.
    def enterCharacterStringValueExpression(self, ctx:spgdsParser.CharacterStringValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#characterStringValueExpression.
    def exitCharacterStringValueExpression(self, ctx:spgdsParser.CharacterStringValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#byteStringValueExpression.
    def enterByteStringValueExpression(self, ctx:spgdsParser.ByteStringValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#byteStringValueExpression.
    def exitByteStringValueExpression(self, ctx:spgdsParser.ByteStringValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimOperands.
    def enterTrimOperands(self, ctx:spgdsParser.TrimOperandsContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimOperands.
    def exitTrimOperands(self, ctx:spgdsParser.TrimOperandsContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimCharacterOrByteStringSource.
    def enterTrimCharacterOrByteStringSource(self, ctx:spgdsParser.TrimCharacterOrByteStringSourceContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimCharacterOrByteStringSource.
    def exitTrimCharacterOrByteStringSource(self, ctx:spgdsParser.TrimCharacterOrByteStringSourceContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimSpecification.
    def enterTrimSpecification(self, ctx:spgdsParser.TrimSpecificationContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimSpecification.
    def exitTrimSpecification(self, ctx:spgdsParser.TrimSpecificationContext):
        pass


    # Enter a parse tree produced by spgdsParser#trimCharacterOrByteString.
    def enterTrimCharacterOrByteString(self, ctx:spgdsParser.TrimCharacterOrByteStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#trimCharacterOrByteString.
    def exitTrimCharacterOrByteString(self, ctx:spgdsParser.TrimCharacterOrByteStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#normalForm.
    def enterNormalForm(self, ctx:spgdsParser.NormalFormContext):
        pass

    # Exit a parse tree produced by spgdsParser#normalForm.
    def exitNormalForm(self, ctx:spgdsParser.NormalFormContext):
        pass


    # Enter a parse tree produced by spgdsParser#stringLength.
    def enterStringLength(self, ctx:spgdsParser.StringLengthContext):
        pass

    # Exit a parse tree produced by spgdsParser#stringLength.
    def exitStringLength(self, ctx:spgdsParser.StringLengthContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeValueExpression.
    def enterDatetimeValueExpression(self, ctx:spgdsParser.DatetimeValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeValueExpression.
    def exitDatetimeValueExpression(self, ctx:spgdsParser.DatetimeValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeValueFunction.
    def enterDatetimeValueFunction(self, ctx:spgdsParser.DatetimeValueFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeValueFunction.
    def exitDatetimeValueFunction(self, ctx:spgdsParser.DatetimeValueFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#dateFunction.
    def enterDateFunction(self, ctx:spgdsParser.DateFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#dateFunction.
    def exitDateFunction(self, ctx:spgdsParser.DateFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#timeFunction.
    def enterTimeFunction(self, ctx:spgdsParser.TimeFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#timeFunction.
    def exitTimeFunction(self, ctx:spgdsParser.TimeFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#localtimeFunction.
    def enterLocaltimeFunction(self, ctx:spgdsParser.LocaltimeFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#localtimeFunction.
    def exitLocaltimeFunction(self, ctx:spgdsParser.LocaltimeFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeFunction.
    def enterDatetimeFunction(self, ctx:spgdsParser.DatetimeFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeFunction.
    def exitDatetimeFunction(self, ctx:spgdsParser.DatetimeFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#localdatetimeFunction.
    def enterLocaldatetimeFunction(self, ctx:spgdsParser.LocaldatetimeFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#localdatetimeFunction.
    def exitLocaldatetimeFunction(self, ctx:spgdsParser.LocaldatetimeFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#dateFunctionParameters.
    def enterDateFunctionParameters(self, ctx:spgdsParser.DateFunctionParametersContext):
        pass

    # Exit a parse tree produced by spgdsParser#dateFunctionParameters.
    def exitDateFunctionParameters(self, ctx:spgdsParser.DateFunctionParametersContext):
        pass


    # Enter a parse tree produced by spgdsParser#timeFunctionParameters.
    def enterTimeFunctionParameters(self, ctx:spgdsParser.TimeFunctionParametersContext):
        pass

    # Exit a parse tree produced by spgdsParser#timeFunctionParameters.
    def exitTimeFunctionParameters(self, ctx:spgdsParser.TimeFunctionParametersContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeFunctionParameters.
    def enterDatetimeFunctionParameters(self, ctx:spgdsParser.DatetimeFunctionParametersContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeFunctionParameters.
    def exitDatetimeFunctionParameters(self, ctx:spgdsParser.DatetimeFunctionParametersContext):
        pass


    # Enter a parse tree produced by spgdsParser#durationValueExpression.
    def enterDurationValueExpression(self, ctx:spgdsParser.DurationValueExpressionContext):
        pass

    # Exit a parse tree produced by spgdsParser#durationValueExpression.
    def exitDurationValueExpression(self, ctx:spgdsParser.DurationValueExpressionContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeSubtraction.
    def enterDatetimeSubtraction(self, ctx:spgdsParser.DatetimeSubtractionContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeSubtraction.
    def exitDatetimeSubtraction(self, ctx:spgdsParser.DatetimeSubtractionContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeSubtractionParameters.
    def enterDatetimeSubtractionParameters(self, ctx:spgdsParser.DatetimeSubtractionParametersContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeSubtractionParameters.
    def exitDatetimeSubtractionParameters(self, ctx:spgdsParser.DatetimeSubtractionParametersContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeValueExpression1.
    def enterDatetimeValueExpression1(self, ctx:spgdsParser.DatetimeValueExpression1Context):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeValueExpression1.
    def exitDatetimeValueExpression1(self, ctx:spgdsParser.DatetimeValueExpression1Context):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeValueExpression2.
    def enterDatetimeValueExpression2(self, ctx:spgdsParser.DatetimeValueExpression2Context):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeValueExpression2.
    def exitDatetimeValueExpression2(self, ctx:spgdsParser.DatetimeValueExpression2Context):
        pass


    # Enter a parse tree produced by spgdsParser#durationValueFunction.
    def enterDurationValueFunction(self, ctx:spgdsParser.DurationValueFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#durationValueFunction.
    def exitDurationValueFunction(self, ctx:spgdsParser.DurationValueFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#durationFunction.
    def enterDurationFunction(self, ctx:spgdsParser.DurationFunctionContext):
        pass

    # Exit a parse tree produced by spgdsParser#durationFunction.
    def exitDurationFunction(self, ctx:spgdsParser.DurationFunctionContext):
        pass


    # Enter a parse tree produced by spgdsParser#durationFunctionParameters.
    def enterDurationFunctionParameters(self, ctx:spgdsParser.DurationFunctionParametersContext):
        pass

    # Exit a parse tree produced by spgdsParser#durationFunctionParameters.
    def exitDurationFunctionParameters(self, ctx:spgdsParser.DurationFunctionParametersContext):
        pass


    # Enter a parse tree produced by spgdsParser#objectName.
    def enterObjectName(self, ctx:spgdsParser.ObjectNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#objectName.
    def exitObjectName(self, ctx:spgdsParser.ObjectNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#objectNameOrBindingVariable.
    def enterObjectNameOrBindingVariable(self, ctx:spgdsParser.ObjectNameOrBindingVariableContext):
        pass

    # Exit a parse tree produced by spgdsParser#objectNameOrBindingVariable.
    def exitObjectNameOrBindingVariable(self, ctx:spgdsParser.ObjectNameOrBindingVariableContext):
        pass


    # Enter a parse tree produced by spgdsParser#directoryName.
    def enterDirectoryName(self, ctx:spgdsParser.DirectoryNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#directoryName.
    def exitDirectoryName(self, ctx:spgdsParser.DirectoryNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#schemaName.
    def enterSchemaName(self, ctx:spgdsParser.SchemaNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#schemaName.
    def exitSchemaName(self, ctx:spgdsParser.SchemaNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphName.
    def enterGraphName(self, ctx:spgdsParser.GraphNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphName.
    def exitGraphName(self, ctx:spgdsParser.GraphNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#delimitedGraphName.
    def enterDelimitedGraphName(self, ctx:spgdsParser.DelimitedGraphNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#delimitedGraphName.
    def exitDelimitedGraphName(self, ctx:spgdsParser.DelimitedGraphNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#graphTypeName.
    def enterGraphTypeName(self, ctx:spgdsParser.GraphTypeNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#graphTypeName.
    def exitGraphTypeName(self, ctx:spgdsParser.GraphTypeNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeTypeName.
    def enterNodeTypeName(self, ctx:spgdsParser.NodeTypeNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeTypeName.
    def exitNodeTypeName(self, ctx:spgdsParser.NodeTypeNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeTypeName.
    def enterEdgeTypeName(self, ctx:spgdsParser.EdgeTypeNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeTypeName.
    def exitEdgeTypeName(self, ctx:spgdsParser.EdgeTypeNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingTableName.
    def enterBindingTableName(self, ctx:spgdsParser.BindingTableNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingTableName.
    def exitBindingTableName(self, ctx:spgdsParser.BindingTableNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#delimitedBindingTableName.
    def enterDelimitedBindingTableName(self, ctx:spgdsParser.DelimitedBindingTableNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#delimitedBindingTableName.
    def exitDelimitedBindingTableName(self, ctx:spgdsParser.DelimitedBindingTableNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#procedureName.
    def enterProcedureName(self, ctx:spgdsParser.ProcedureNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#procedureName.
    def exitProcedureName(self, ctx:spgdsParser.ProcedureNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#labelName.
    def enterLabelName(self, ctx:spgdsParser.LabelNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#labelName.
    def exitLabelName(self, ctx:spgdsParser.LabelNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#propertyName.
    def enterPropertyName(self, ctx:spgdsParser.PropertyNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#propertyName.
    def exitPropertyName(self, ctx:spgdsParser.PropertyNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#fieldName.
    def enterFieldName(self, ctx:spgdsParser.FieldNameContext):
        pass

    # Exit a parse tree produced by spgdsParser#fieldName.
    def exitFieldName(self, ctx:spgdsParser.FieldNameContext):
        pass


    # Enter a parse tree produced by spgdsParser#elementVariable.
    def enterElementVariable(self, ctx:spgdsParser.ElementVariableContext):
        pass

    # Exit a parse tree produced by spgdsParser#elementVariable.
    def exitElementVariable(self, ctx:spgdsParser.ElementVariableContext):
        pass


    # Enter a parse tree produced by spgdsParser#pathVariable.
    def enterPathVariable(self, ctx:spgdsParser.PathVariableContext):
        pass

    # Exit a parse tree produced by spgdsParser#pathVariable.
    def exitPathVariable(self, ctx:spgdsParser.PathVariableContext):
        pass


    # Enter a parse tree produced by spgdsParser#subpathVariable.
    def enterSubpathVariable(self, ctx:spgdsParser.SubpathVariableContext):
        pass

    # Exit a parse tree produced by spgdsParser#subpathVariable.
    def exitSubpathVariable(self, ctx:spgdsParser.SubpathVariableContext):
        pass


    # Enter a parse tree produced by spgdsParser#bindingVariable.
    def enterBindingVariable(self, ctx:spgdsParser.BindingVariableContext):
        pass

    # Exit a parse tree produced by spgdsParser#bindingVariable.
    def exitBindingVariable(self, ctx:spgdsParser.BindingVariableContext):
        pass


    # Enter a parse tree produced by spgdsParser#unsignedLiteral.
    def enterUnsignedLiteral(self, ctx:spgdsParser.UnsignedLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#unsignedLiteral.
    def exitUnsignedLiteral(self, ctx:spgdsParser.UnsignedLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#generalLiteral.
    def enterGeneralLiteral(self, ctx:spgdsParser.GeneralLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#generalLiteral.
    def exitGeneralLiteral(self, ctx:spgdsParser.GeneralLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#temporalLiteral.
    def enterTemporalLiteral(self, ctx:spgdsParser.TemporalLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#temporalLiteral.
    def exitTemporalLiteral(self, ctx:spgdsParser.TemporalLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#dateLiteral.
    def enterDateLiteral(self, ctx:spgdsParser.DateLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#dateLiteral.
    def exitDateLiteral(self, ctx:spgdsParser.DateLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#timeLiteral.
    def enterTimeLiteral(self, ctx:spgdsParser.TimeLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#timeLiteral.
    def exitTimeLiteral(self, ctx:spgdsParser.TimeLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeLiteral.
    def enterDatetimeLiteral(self, ctx:spgdsParser.DatetimeLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeLiteral.
    def exitDatetimeLiteral(self, ctx:spgdsParser.DatetimeLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#listLiteral.
    def enterListLiteral(self, ctx:spgdsParser.ListLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#listLiteral.
    def exitListLiteral(self, ctx:spgdsParser.ListLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#recordLiteral.
    def enterRecordLiteral(self, ctx:spgdsParser.RecordLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#recordLiteral.
    def exitRecordLiteral(self, ctx:spgdsParser.RecordLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#identifier.
    def enterIdentifier(self, ctx:spgdsParser.IdentifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#identifier.
    def exitIdentifier(self, ctx:spgdsParser.IdentifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#regularIdentifier.
    def enterRegularIdentifier(self, ctx:spgdsParser.RegularIdentifierContext):
        pass

    # Exit a parse tree produced by spgdsParser#regularIdentifier.
    def exitRegularIdentifier(self, ctx:spgdsParser.RegularIdentifierContext):
        pass


    # Enter a parse tree produced by spgdsParser#timeZoneString.
    def enterTimeZoneString(self, ctx:spgdsParser.TimeZoneStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#timeZoneString.
    def exitTimeZoneString(self, ctx:spgdsParser.TimeZoneStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#characterStringLiteral.
    def enterCharacterStringLiteral(self, ctx:spgdsParser.CharacterStringLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#characterStringLiteral.
    def exitCharacterStringLiteral(self, ctx:spgdsParser.CharacterStringLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#unsignedNumericLiteral.
    def enterUnsignedNumericLiteral(self, ctx:spgdsParser.UnsignedNumericLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#unsignedNumericLiteral.
    def exitUnsignedNumericLiteral(self, ctx:spgdsParser.UnsignedNumericLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#exactNumericLiteral.
    def enterExactNumericLiteral(self, ctx:spgdsParser.ExactNumericLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#exactNumericLiteral.
    def exitExactNumericLiteral(self, ctx:spgdsParser.ExactNumericLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#approximateNumericLiteral.
    def enterApproximateNumericLiteral(self, ctx:spgdsParser.ApproximateNumericLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#approximateNumericLiteral.
    def exitApproximateNumericLiteral(self, ctx:spgdsParser.ApproximateNumericLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#unsignedInteger.
    def enterUnsignedInteger(self, ctx:spgdsParser.UnsignedIntegerContext):
        pass

    # Exit a parse tree produced by spgdsParser#unsignedInteger.
    def exitUnsignedInteger(self, ctx:spgdsParser.UnsignedIntegerContext):
        pass


    # Enter a parse tree produced by spgdsParser#unsignedDecimalInteger.
    def enterUnsignedDecimalInteger(self, ctx:spgdsParser.UnsignedDecimalIntegerContext):
        pass

    # Exit a parse tree produced by spgdsParser#unsignedDecimalInteger.
    def exitUnsignedDecimalInteger(self, ctx:spgdsParser.UnsignedDecimalIntegerContext):
        pass


    # Enter a parse tree produced by spgdsParser#nullLiteral.
    def enterNullLiteral(self, ctx:spgdsParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#nullLiteral.
    def exitNullLiteral(self, ctx:spgdsParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#dateString.
    def enterDateString(self, ctx:spgdsParser.DateStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#dateString.
    def exitDateString(self, ctx:spgdsParser.DateStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#timeString.
    def enterTimeString(self, ctx:spgdsParser.TimeStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#timeString.
    def exitTimeString(self, ctx:spgdsParser.TimeStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#datetimeString.
    def enterDatetimeString(self, ctx:spgdsParser.DatetimeStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#datetimeString.
    def exitDatetimeString(self, ctx:spgdsParser.DatetimeStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#durationLiteral.
    def enterDurationLiteral(self, ctx:spgdsParser.DurationLiteralContext):
        pass

    # Exit a parse tree produced by spgdsParser#durationLiteral.
    def exitDurationLiteral(self, ctx:spgdsParser.DurationLiteralContext):
        pass


    # Enter a parse tree produced by spgdsParser#durationString.
    def enterDurationString(self, ctx:spgdsParser.DurationStringContext):
        pass

    # Exit a parse tree produced by spgdsParser#durationString.
    def exitDurationString(self, ctx:spgdsParser.DurationStringContext):
        pass


    # Enter a parse tree produced by spgdsParser#nodeSynonym.
    def enterNodeSynonym(self, ctx:spgdsParser.NodeSynonymContext):
        pass

    # Exit a parse tree produced by spgdsParser#nodeSynonym.
    def exitNodeSynonym(self, ctx:spgdsParser.NodeSynonymContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgesSynonym.
    def enterEdgesSynonym(self, ctx:spgdsParser.EdgesSynonymContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgesSynonym.
    def exitEdgesSynonym(self, ctx:spgdsParser.EdgesSynonymContext):
        pass


    # Enter a parse tree produced by spgdsParser#edgeSynonym.
    def enterEdgeSynonym(self, ctx:spgdsParser.EdgeSynonymContext):
        pass

    # Exit a parse tree produced by spgdsParser#edgeSynonym.
    def exitEdgeSynonym(self, ctx:spgdsParser.EdgeSynonymContext):
        pass


    # Enter a parse tree produced by spgdsParser#nonReservedWords.
    def enterNonReservedWords(self, ctx:spgdsParser.NonReservedWordsContext):
        pass

    # Exit a parse tree produced by spgdsParser#nonReservedWords.
    def exitNonReservedWords(self, ctx:spgdsParser.NonReservedWordsContext):
        pass



del spgdsParser