# Hello World
# Created by Thomas Lobker
#
# This is a simple contract to demonstrate
# how to deploy and invoke a contract

# NEO API includes
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness, Notify, Log
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Enumerator import EnumeratorCreate, EnumeratorNext

# Compiler includes
from boa.builtins import concat


def Main(operation, arguments):
    print("Running DNS contract v1")
    trigger = GetTrigger()

    if len(arguments) < 1 or (operation == 'put' and len(arguments) < 2):
        return False

    if not is_valid_addr(arguments[0]):
        return False

    # This determines that the SC is running in Verification mode
    # This determines whether the TX will be relayed to the rest of the network
    # The `Verification` portion of SC is *read-only*, so calls to `Storage.Put` will fail.
    # You can, however, use `Storage.Get`
    if trigger == Verification():

        print("Running Verification!")
        if operation == 'put' or operation == 'delete':
            return CheckWitness(arguments[0])
        elif operation == 'get':
            return True

        return False

    elif trigger == Application():

        print("Running Application!")

        ctx = GetContext()

        if operation == 'put':
            Put(ctx, arguments[0], arguments[1])
            return True
        elif operation == 'get':
            return Get(ctx, arguments[0])
        elif operation == 'delete':
            Delete(ctx, arguments[0])
            return True

        return False

    return False


def is_valid_addr(addr):
    if len(addr) == 20:
        return True
    return False

