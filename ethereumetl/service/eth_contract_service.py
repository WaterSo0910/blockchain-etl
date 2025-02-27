# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from typing import Optional, List, Union

import logging

from hexbytes.main import HexBytes
from eth_utils.abi import function_signature_to_4byte_selector
from ethereum_dasm.evmdasm import EvmCode, Contract
from ethereumetl.domain.contract import EthContract
from web3 import Web3

# ref https://github.com/blockchain-etl/ethereum-etl/pull/267
logging.getLogger("ethereum_dasm.evmdasm").setLevel(logging.ERROR)
logging.getLogger("evmdasm.disassembler").setLevel(logging.FATAL)


class EthContractService:
    def __init__(self, web3: Optional[Web3] = None):
        self.web3 = web3

    def get_function_sighashes(
        self, bytecode: Optional[Union[str, HexBytes]]
    ) -> List[str]:
        bytecode = clean_bytecode(bytecode)
        if bytecode is None:
            return []

        evm_code = EvmCode(
            contract=Contract(bytecode=bytecode),
            static_analysis=False,
            dynamic_analysis=False,
        )
        evm_code.disassemble(bytecode)
        basic_blocks = evm_code.basicblocks

        # store from https://github.com/blockchain-etl/ethereum-etl/pull/282
        push4_instructions = set()
        for block in basic_blocks:
            for inst in block.instructions:
                if inst.name == "PUSH4":
                    push4_instructions.add("0x" + inst.operand)
        return sorted(push4_instructions)

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
    # https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/ERC20.sol
    def is_erc20_contract(self, function_sighashes: List[str]):
        c = ContractWrapper(function_sighashes)
        return (
            c.implements("totalSupply()")
            and c.implements("decimals()")
            and c.implements("balanceOf(address)")
            and c.implements("transfer(address,uint256)")
            and c.implements("transferFrom(address,address,uint256)")
            and c.implements("approve(address,uint256)")
            and c.implements("allowance(address,address)")
            and not c.implements("tokenURI(uint256)")
        )

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md
    # https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC721/ERC721Basic.sol
    # Doesn't check the below ERC721 methods to match CryptoKitties contract
    # getApproved(uint256)
    # setApprovalForAll(address,bool)
    # isApprovedForAll(address,address)
    # transferFrom(address,address,uint256)
    # safeTransferFrom(address,address,uint256)
    # safeTransferFrom(address,address,uint256,bytes)
    def is_erc721_contract(self, function_sighashes: List[str]):
        c = ContractWrapper(function_sighashes)
        return (
            c.implements("balanceOf(address)")
            and c.implements("ownerOf(uint256)")
            and c.implements_any_of(
                "transfer(address,uint256)",
                "transferFrom(address,address,uint256)",
                "safeTransferFrom(address,address,uint256)",
                "safeTransferFrom(address,address,uint256,bytes)",
            )
            and c.implements("approve(address,uint256)")
            and not c.implements("decimals()")
        )

    def get_contract(self, contract_address: str, block_id=None):
        assert self.web3 is not None

        checksum_address = Web3.toChecksumAddress(contract_address)
        contract_code = self.web3.eth.get_code(checksum_address, block_id).hex()
        if contract_code == "0x":
            return None

        contract = EthContract()
        contract.address = contract_address.lower()
        contract.bytecode = contract_code
        function_sighashes = self.get_function_sighashes(contract.bytecode)

        contract.function_sighashes = function_sighashes
        contract.is_erc20 = self.is_erc20_contract(function_sighashes)
        contract.is_erc721 = self.is_erc721_contract(function_sighashes)

        return contract


def clean_bytecode(bytecode: Optional[Union[str, HexBytes]]) -> Optional[str]:
    if isinstance(bytecode, HexBytes):
        bytecode = bytecode.hex()

    if bytecode is None or bytecode == "0x":
        return None
    elif bytecode.startswith("0x"):
        return bytecode[2:]
    else:
        return bytecode


def get_function_sighash(signature: str) -> str:
    return "0x" + function_signature_to_4byte_selector(signature).hex()


class ContractWrapper:
    def __init__(self, sighashes):
        self.sighashes = sighashes

    def implements(self, function_signature: str) -> bool:
        sighash = get_function_sighash(function_signature)
        return sighash in self.sighashes

    def implements_any_of(self, *function_signatures) -> bool:
        return any(
            self.implements(function_signature)
            for function_signature in function_signatures
        )
