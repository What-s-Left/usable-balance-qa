import Data from './helpers/data'
import Funcs from './helpers/func'

import {EntitiesMatch} from './entities/match'


async function init() {

    await EntitiesMatch.setup_listeners()

    console.log("Usable Balance App - Ready :)");

}


await init();

// QA - Entities Match

