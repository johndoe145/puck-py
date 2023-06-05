#
#    Copyright (C) 2022 Alfred Daimari
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#

import json
from typing import List
from .yd_config import YdStickConfig


class BitPack:
    """
    data structure to hold a row of bits \n
    --- \n

    attributes: \n
    bpk - (bit packet) a row of bitbuffer received from rtl_433, \n
    time_to_prev_bpk - gap to the previous row of bitbuffer \n
    --- \n

    methods: \n
    convert_to_hex() \n
    convert_to_binary() \n
    convert_to_decimal() \n
    """

    def __init__(self, bpk: str, gap_to_prev_bpk: int) -> None:
        """
        init bit packet \n
        :param bpk: a string of bits, duh!
        :param gap_to_prev_bpk: gap to previous row in bitbuffer, generated by rtl_433
        """
        self.time_to_prev_bitpk = gap_to_prev_bpk / 250000  # might not need this, remove ?
        self.bpk = bpk
        self.__num_type = 2  # numeral system used to represent the bit_pk

    def __str__(self) -> str:
        return self.bpk

    def __len__(self) -> int:
        return len(self.bpk)

    def bpk_drop(self, pos: int) -> None:
        """
        drops all bits from pos \n
        :param pos: dropping index
        """
        self.bpk = self.bpk[:pos]

    def bpk_pad(self, num0: int) -> None:
        """
        :param num0: number of 0s to pad
        :return: None
        """
        self.bpk += ("0" * num0)

    def convert_to_hex(self) -> None:
        """
        Converts binary to hex
        """
        if self.__num_type == 2:
            int_rep = int(self.bpk, 2)
            hex_rep = hex(int_rep)
            self.bpk = hex_rep[2:]
            self.__num_type = 16

        if self.__num_type == 10:
            hex_rep = hex(self.bpk)
            self.bpk = hex_rep[2:]
            self.__num_type = 16

    def convert_to_binary(self) -> None:
        """
        Converts to binary
        """
        if self.__num_type == 16:
            int_rep = int(self.bpk, 16)
            bin_rep = bin(int_rep)[2:]
            self.bpk = bin_rep
            self.__num_type = 2

        if self.__num_type == 10:
            bin_rep = bin(self.bpk)[2:]
            self.bpk = bin_rep
            self.__num_type = 2

    def convert_to_decimal(self) -> None:
        """
        Converts to decimal
        """
        if self.__num_type == 16:
            int_rep = int(self.bpk, 16)
            self.bpk = int_rep
            self.__num_type = 10

        if self.__num_type == 2:
            int_rep = int(self.bpk, 2)
            self.bpk = int_rep
            self.__num_type = 10


class KeyFobPacket:
    """
    data structure to hold a key fob packet \n
    --- \n

    attributes: \n
    packets: instances of BitPackets \n
    pk_recv_time: the time received (unix time ns format)
    """

    def __init__(self, cfg: YdStickConfig, kfb_list: List[str], kfb_type: str, bpk_recv_time: int) -> None:
        """
        :param cfg: yd_stick configuration
        :param kfb_list: ['1000101:0', '1010101:45'] format
        :param kfb_type: key fob type
        :param bpk_recv_time: time bpk was received in unix ns
        """
        self.kfb_type = kfb_type

        bpk_split = [kfb_row.split(':') for kfb_row in
                     kfb_list]  # -> [['1001', '0'], ['11001', '18']] (split into b_row, gap)
        self.bpk_list = [BitPack(bpk_s[0], int(bpk_s[1])) for bpk_s in bpk_split]

        self.bpk_recv_time = bpk_recv_time
        self.cfg = cfg

    def __len__(self):
        return len(self.bpk_list)

    def __str__(self):
        str_ = ""
        for i in range(len(self.bpk_list)):
            str_ += self.bpk_list[i].__str__() + f" ----- {i + 1}\n"
        return str_

    def __clean(self):
        pass

    def to_kfb_str(self) -> List[str]:
        """
        converts back to kfb str rep
        :return: ["bits:time", "bits:time"]
        """
        tmp_kfb_list = []
        for bpk in self.bpk_list:
            tmp_kfb_list.append(f"{str(bpk)}:{bpk.time_to_prev_bitpk}")
        return tmp_kfb_list

    def convert_to_hex(self) -> None:
        """
        Converts bits to hex representation
        """
        for bpk in self.bpk_list:
            bpk.convert_to_hex()

    def convert_to_binary(self) -> None:
        """
        Converts bits to binary representation
        """
        for bpk in self.bpk_list:
            bpk.convert_to_binary()

    def convert_to_decimal(self) -> None:
        """
        Converts bits to decimal representation
        """
        for bpk in self.bpk_list:
            bpk.convert_to_decimal()

    def concat_bpk_list(self) -> str:
        """
        :return: string of concatenated packets (performs this after hex conversion)
        """
        pass

    @classmethod
    def filter(cls, kfb_bb: List[str]) -> List[List[str]]:
        """
        :param kfb_bb: key fob bit buffer
        :return: list of kfb_bb
        """
        pass
