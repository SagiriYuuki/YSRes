from kaitaistruct import KaitaiStream
from io import BytesIO
import glob, os, sys, json
import subprocess

sys.path.append("./py")
from textmap import Textmap

# Change TextMapLanguage
TextMapLanguage = "KR"
'''
    01/26692920 => 
    02/27251172 => 
    03/25181351 => 
    04/25776943 => EN
    05/20618174 => 
    06/25555476 => 
    07/30460104 => 
    08/32244380 => 
    09/22299426 => KR
    10/23331191 => 
    11/21030516 => 
    12/32056053 => 
    13/34382464 => 
'''

def GetAllTextmaps():
    global TextMapLanguage
    output = dict()

    total = len(glob.glob('./bin/TextMap_' + TextMapLanguage + '/*.bin'))
    cnt = 0

    for file in glob.glob('./bin/TextMap_' + TextMapLanguage + '/*.bin'):

        cnt += 1
        print("Parsing in progress [" + str(cnt) + "/" + str(total) + "]")

        with open(file, 'rb') as f:
            stream = KaitaiStream(BytesIO(f.read()))
            obj = Textmap(stream)

            for block in obj.textmap:
                output[str(block.hash.value)] = block.string.data

    with open("./json/TextMap_" + TextMapLanguage + ".json", "w", encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)

def DumpAvatarExcel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarExcelConfigData.bin', './ksy/avatar_excel.ksy']

    with open('./json/Dump_AvatarExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def ParseAvatarExcel():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            if block["has_field_use_type"]:
                output_block["useType"] = block["use_type"]["value"][16:].upper()
            
            output_block["bodyType"] = block["body_type"]["value"][10:].upper()
            output_block["iconName"] = block["icon_name"]["data"]
            output_block["sideIconName"] = block["side_icon_name"]["data"]
            output_block["qualityType"] = block["quality_type"]["value"][13:].upper()
            output_block["chargeEfficiency"] = block["charge_efficiency"]

            if block["has_field_is_range_attack"]:
                output_block["isRangeAttack"] = block["is_range_attack"]

            output_block["initialWeapon"] = block["initial_weapon"]["value"]
            output_block["weaponType"] = block["weapon_type"]["value"][12:].upper()
            output_block["imageName"] = block["image_name"]["data"]
            output_block["cutsceneShow"] = block["cutscene_show"]["data"]
            output_block["skillDepotId"] = block["skill_depot_id"]["value"]
            output_block["staminaRecoverSpeed"] = block["stamina_recover_speed"]
            output_block["candSkillDepotIds"] = [i["value"] for i in block["cand_skill_depot_ids"]["data"]]
            output_block["manekinMotionConfig"] = block["manekin_motion_config"]["value"]
            output_block["descTextMapHash"] = block["desc"]["value"]

            if block["has_field_avatar_identity_type"]:
                output_block["avatarIdentityType"] = block["avatar_identity_type"]["value"][21:].upper()
            
            output_block["avatarPromoteId"] = block["avatar_promote_id"]["value"]
            output_block["avatarPromoteRewardLevelList"] = [i["value"] for i in block["avatar_promote_reward_level_list"]["data"]]
            output_block["avatarPromoteRewardIdList"] = [i["value"] for i in block["avatar_promote_reward_id_list"]["data"]]
            output_block["featureTagGroupID"] = block["feature_tag_group_id"]["value"]
            output_block["infoDescTextMapHash"] = block["info_desc"]["value"]
            output_block["hpBase"] = block["hp_base"]
            output_block["attackBase"] = block["attack_base"]
            output_block["defenseBase"] = block["defense_base"]
            output_block["critical"] = block["critical"]
            output_block["criticalHurt"] = block["critical_hurt"]

            prop_grow_curves = []
            for i in block["prop_grow_curves"]["data"]:
                prop_grow = dict()
                prop_grow["type"] = i["type"]["value"][16:].upper()
                prop_grow["growCurve"] = i["grow_curve"]["value"][16:].upper()
                prop_grow_curves.append(prop_grow)
            output_block["propGrowCurves"] = prop_grow_curves

            output_block["id"] = block["id"]["value"]
            output_block["nameTextMapHash"] = block["name"]["value"]
            output_block["LODPatternName"] = block["lod_pattern_name"]["data"]

            output.append(output_block)

    with open('./json/AvatarExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)

# GetAllTextmaps()
# DumpAvatarExcel()
# ParseAvatarExcel()