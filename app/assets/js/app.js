import Data from './helpers/data'
import Funcs from './helpers/func'

import {EntitiesMatch} from './entities/match'
import {EntitiesManage} from "./entities/manage";

async function init() {

    await EntitiesMatch.setup_listeners()
    await EntitiesManage.setup_listeners()

    console.log("Usable Balance App - Ready :)");

}

await init();
