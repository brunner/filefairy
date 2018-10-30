#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/team', '', _path))
from util.jersey.jersey import get_rawid  # noqa


class TeamTest(unittest.TestCase):
    def test_decoding_to_encoding(self):
        self.assertEqual(
            get_rawid('angels'),
            '9780ce2762db67b17831a0c908aaf725/raw/1018f1ba85a160d74d5a924749a6cd28cae44a40'
        )
        self.assertEqual(
            get_rawid('astros'),
            '2d3444f09ba1f0c9a06b6e9bdd27eda7/raw/b19253b93017682124fe778e0a8624c12bcc6332'
        )
        self.assertEqual(
            get_rawid('athletics'),
            '5641c5488e3de552ebd8f04c7d089fd9/raw/f62eb1e611dcb85832aa9cfc2ea1165a99325beb'
        )
        self.assertEqual(
            get_rawid('bluejays'),
            '75833b35b51c8b6cd5c300e0d4117739/raw/ac65ce092e906593e512d3452a38c2e5668f8447'
        )
        self.assertEqual(
            get_rawid('braves'),
            '70fe783889494c2c0de8cd9b2dbd05b2/raw/af5e8226f04e295506a61636aaf6d405c6d24a54'
        )
        self.assertEqual(
            get_rawid('brewers'),
            '5aa56738ca8fc3f8367d6f777614de38/raw/854c03ddbbd38842ee7e62f825b0dcd97cb9d391'
        )
        self.assertEqual(
            get_rawid('cardinals'),
            '2f8467f7cef50d56217cd0bd4da65ca0/raw/b854738755e6572c1aec7ca65a16b1030a4c3b53'
        )
        self.assertEqual(
            get_rawid('cubs'),
            'ed81fde94a24fdce340a19e52fda33bd/raw/cf6811a0707e24be1ef2038f91cc295525274cf6'
        )
        self.assertEqual(
            get_rawid('diamondbacks'),
            '925f81153b44d0b35734ca0c43b9f89a/raw/e46d3919da84e127c46ddb9a98083fdfe45c550e'
        )
        self.assertEqual(
            get_rawid('dodgers'),
            'd334f966fa470e01991d550266b94283/raw/4572edb247c3b7281f01cf01e0ee97f34a14e145'
        )
        self.assertEqual(
            get_rawid('giants'),
            'd82f716325270e162d646bbaa7160c8b/raw/f5c7a0e63b18cfaef3aff919f1c74d60719f5747'
        )
        self.assertEqual(
            get_rawid('indians'),
            '40b0331a059d0ad8869df7e101863401/raw/39c4825ca85027191a3003528ce36ab6c85bf537'
        )
        self.assertEqual(
            get_rawid('mariners'),
            '146290fc1036d7628d016218e9a05a92/raw/6a6f13694db39de9d335e25661138a4f14ccf4ab'
        )
        self.assertEqual(
            get_rawid('marlins'),
            '793744dc81800fea7f219dd22b28afa1/raw/b2fe8e13546351a7272f1b90d066b398620adcac'
        )
        self.assertEqual(
            get_rawid('mets'),
            'aa9197d99dd2abcb7a50f13e5ae75ab0/raw/b209622a6f5849a60035cd3f583914bb557fb514'
        )
        self.assertEqual(
            get_rawid('nationals'),
            '7364eac50fccbb97ce1ea034da8e3c6a/raw/47d7dae296e3b5d262e9dca3effad546969670f1'
        )
        self.assertEqual(
            get_rawid('orioles'),
            '6df0d030fbb62f9cd169624afe5351e3/raw/f9576bb0aa8427c19832bb972962b86c3a6cb1f2'
        )
        self.assertEqual(
            get_rawid('padres'),
            'a2ae8f3ef490bad2f2f5510428d4bdc2/raw/b9c65c44cca5eab7453ae85ac728e27ae7416b67'
        )
        self.assertEqual(
            get_rawid('phillies'),
            '21cdbe29a981ae9e9eeeccbd93b7e76e/raw/44bdf456e169c959be199c0030228077a7104c1e'
        )
        self.assertEqual(
            get_rawid('pirates'),
            'b52b416175cd704f7dd007d890dd629e/raw/a3771c5794f7677c45b99bc467af7fa87ab26d6d'
        )
        self.assertEqual(
            get_rawid('rangers'),
            '468cead9ea12e6bb3ba6f62236b8d1a7/raw/80fb2958b8e027e2d8a8097bcb7cd4b3bd9bfe13'
        )
        self.assertEqual(
            get_rawid('rays'),
            '72da90820a526e10bad1484efd2aaea3/raw/9596cda701c2d5af036d726e2547db65dfcda134'
        )
        self.assertEqual(
            get_rawid('reds'),
            'af532f33900c377ea6a7d5c373a9785f/raw/8eb50b108f9f65dfcc71b30ddb3b9ab032a972c1'
        )
        self.assertEqual(
            get_rawid('redsox'),
            '4a6a4036834b558756dac7ac9c0309d0/raw/b370f4842d7d271d9935f30d231abe0368409944'
        )
        self.assertEqual(
            get_rawid('rockies'),
            '79886209567ba70e64192b9810bde6a3/raw/ed1def95cd767f6c4e0601b6dd440d58f365e894'
        )
        self.assertEqual(
            get_rawid('royals'),
            'f87f4b6bf4821f16ef57eae0823e9fc7/raw/1f8528c7ec317d89f3e7ba6de2b3c3dd7340f64c'
        )
        self.assertEqual(
            get_rawid('tigers'),
            '89a0edfe4287648effd8021807ef9625/raw/2a80951e810dccdb569fc2f249e3fb8c00675000'
        )
        self.assertEqual(
            get_rawid('twins'),
            '5b5568f5e186885d5e5175a25959f5d0/raw/278276af922a94ee6396cace99f17c3a308da730'
        )
        self.assertEqual(
            get_rawid('whitesox'),
            '359d34636fabc914a83a8c746fc6eba9/raw/1afa211b3cec808c7d58863fd61d436bbdbe05da'
        )
        self.assertEqual(
            get_rawid('yankees'),
            '5b8b9a01333351a92f6f91726dce239b/raw/0cfd7978330ee9e4c4c4fa37439b9abb903be46a'
        )


if __name__ == '__main__':
    unittest.main()
