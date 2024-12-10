let reverie, map;

class NPCBuilder {
  constructor(name = "NPC", x = -1, y = -1) {
    this.name = name;
    this.x = x;
    this.y = y;

    this.is;

    this.appearance = false;
    this.caller = "";

    this.property = {
      key: this.name,
      moveSpeed: 30,
      useDirAnim: true,
      impassable: true,
      collide: true,
      offsetX: 0,
      offsetY: -20,
      oberlap: false,
      npcProperty: { name: this.name },
    };

    this.sprite = {
      "Dylan Yoon": "DylanYoon.png",
      "Emily Parker": "EmilyParker.png",
      "Helen Potter": "HelenPotter.png",
      "Johnny Kim": "JohnnyKim.png",
      "Reynolds Liam": "Reynolds Liam.png",
      "Elowen Hart": "ElowenHart.png",
      "Ethan Reed": "EthanReed.png",
      "James Mond": "JamesMond.png",
      "Rain Forest": "RainForest.png",
      "Tina Thompson": "TinaThompson.png",
    };

    this.load_sprite(this.sprite[this.name]);
    this.build();
  }

  build() {
    if (this.x < 0 || this.y < 0) return;
    Map.putObjectWithKey(this.x, this.y, this.sprite, this.property);

    this.updateProperty();
    this.getLoc();
    this.appearance = true;
  }

  load_sprite(spriteName) {
    this.sprite = App.loadSpritesheet(
      spriteName,
      30,
      32,
      {
        left: [3, 4, 5], // 좌방향 이동 이미지
        up: [9, 10, 11],
        down: [0, 1, 2],
        right: [6, 7, 8],
      },
      8
    );
  }

  updateProperty() {
    this.property = Map.getObjectWithKey(this.name);
    return this.property;
  }

  //   get location of npc
  getLoc() {
    this.updateProperty();
    let { tileX, tileY } = this.property;

    this.x = tileX;
    this.y = tileY;

    return { x: this.x, y: this.y };
  }

  sayBallon(message) {
    Map.sayObjectWithKey(this.name, message);
  }

  sayToAll(message) {
    App.sayToAll(`[ ${this.name} ] ${message}`, 0xe0e0e0);
  }

  move(x, y) {
    return Map.moveObjectWithKey(this.name, x, y, true);
  }

  responseToPlayer(text) {
    let numbers = text.split(" ");

    // 배열의 각 요소를 숫자로 변환하여 x와 y에 할당
    let x = parseInt(numbers[0], 10);
    let y = parseInt(numbers[1], 10);

    this.move(x, y);

    // this.sayToAll(text);
    this.sayBallon(`(${x}, ${y})로 이동합니다.`);
  }

  destruct() {
    Map.putObjectWithKey(this.x, this.y, null, { key: this.name });
  }

  /*Check if the NPC is on the map*/
  isAppear() {
    return this.appearance;
  }

  chatGPT_parse(url, body, callback) {
    App.httpPostJson(url, {}, body, (res) => {
      App.sayToAll(`${res}`, 0xffffff);
      // 요청 결과를 JSON 오브젝트로 변환
      let response = JSON.parse(res);
      App.sayToAll(`보낸 데이터: ${response.data.name}`, 0xffffff);
    });
  }
}

class systemGAgent {
  constructor() {
    this.api_url = "http://baculum.i234.me:8509";
    // this.api_key = "ga-b696fcb5ef00f7921ca69f0447993254"
    this.reverie;
    this.map;
    this.httpPostJson(
      "http://baculum.i234.me:8509/sendfile/",
      {},
      { filename: "concated_json.json" },
      function (response) {
        reverie = response;
      }
    );
    this.map = this.httpPostJson(
      "http://baculum.i234.me:8509/sendfile/",
      {},
      {
        filename: "mapping_tree.json",
      },
      function (response) {
        map = response;
      }
    );

    this.map_xrange = [2, 95];
    this.map_yrange = [14, 52];
    this.map_xrange_json = [42, 140];
    this.map_yrange_json = [0, 56];
    this._npcs = {};
  }

  httpget(url, headers = null, callback) {
    let response;
    App.httpGet(url, headers, function (res) {
      // 응답 결과를 JSON 오브젝트로 변경
      response = JSON.parse(res);
      // player.name = response;
      // player.sendUpdated();
    });
    return response;
  }

  httpPostJson(url, header, body, callback) {
    App.httpPostJson(url, header, body, (res) => {
      try {
        const response = JSON.parse(res);

        if (response) {
          callback(response);
        } else {
          App.sayToAll("Error: undefined response");
        }
      } catch (error) {
        App.sayToAll(`Error: ${error}`);
      }
      // 요청 결과를 JSON 오브젝트로 변환
    });
  }

  // httpPostJson(url, header, body) {
  //   let response;
  //   App.httpPostJson(url, header, body, (res) => {
  //     // 요청 결과를 JSON 오브젝트로 변환
  //     response = JSON.parse(res);
  //   });
  //   return response;
  // }

  // movement 0.json; place npc on the initial location
  init() {
    this.npc_namelist = this.reverie.metadata.persona_names;
    this.filelist = this.reverie.filelist;
    this.coordinates = this.map.coordinate;
    this.currentCor = {};
    this.map = this.map.map;
    this.count = 0;
    for (let cor of this.coordinates) {
      this.currentCor[cor] = false;
    }

    let perso,
      keys,
      loc,
      x = 20,
      y = 46;
    for (let key of this.npc_namelist) {
      this._npcs[key] = new NPCBuilder(key);

      keys = Object.keys(this.currentCor);
      while (this.currentCor[`[${x}, ${y}]`]) {
        const value = keys[Math.floor(Math.random() * keys.length)]
          .replace(/[\[\]]/g, "")
          .split(",");
        x = parseInt(value[0], 10);
        y = parseInt(value[1], 10);
      }
      this._npcs[key].x = x;
      this._npcs[key].y = y;
      this.currentCor[`[${x}, ${y}]`] = true;
      this._npcs[key].build();
    }
  }

  run() {
    this.count++;
    for (let key of this.npc_namelist) {
      const npc = this._npcs[key];
      let [x, y] = [npc.x, npc.y];

      const keys = Object.keys(this.currentCor);
      while (this.currentCor[`[${x}, ${y}]`]) {
        const value = keys[Math.floor(Math.random() * keys.length)]
          .replace(/[\[\]]/g, "")
          .split(",");
        x = parseInt(value[0], 10);
        y = parseInt(value[1], 10);
      }
      this.npcMove(npc, x, y);
    }
  }

  calculateDistance(x1, y1, x2, y2) {
    const deltaX = x2 - x1;
    const deltaY = y2 - y1;
    return Math.sqrt(deltaX * deltaX + deltaY * deltaY);
  }


  // module(step) {
  //   let curr;
  //   curr = this.filelist[`step_${step}`];

  //   for (let key of this.npc_namelist) {
  //     const npc = this._npcs[key];
  //     if (!npc.isAppear()) {
  //       perso = curr.persona[key];
  //       loc = perso.description;
  //       const loc_list = this.getLocJson(loc);
  //       if (loc_list.includes("prometheus gallery")) {
  //         npc.x = 27;
  //         npc.y = 52;
  //         npc.build();
  //         if (perso.chat == null) {
  //           [x, y] = this.getCoordinates(loc_list);
  //           const keys = Object.keys(this.currentCor);
  //           while (this.currentCor[`[${x}, ${y}]`]) {
  //             const value = keys[Math.floor(Math.random() * keys.length)]
  //               .replace(/[\[\]]/g, "")
  //               .split(",");
  //             x = parseInt(value[0], 10);
  //             y = parseInt(value[1], 10);
  //           }
  //           this.npcMove(npc, x, y, true, false);
  //         } else {
  //           [x, y] = perso.movement;
  //           x = x - this.map_xrange_json[0];
  //           y = y - 4;
  //           npc.move(x, y);
  //         }
  //       }
  //     } else {
  //       if (perso.chat == null) {
  //         [x, y] = this.getCoordinates(loc_list);
  //         const keys = Object.keys(this.currentCor);
  //         while (this.currentCor[`[${x}, ${y}]`]) {
  //           const value = keys[Math.floor(Math.random() * keys.length)]
  //             .replace(/[\[\]]/g, "")
  //             .split(",");
  //           x = parseInt(value[0], 10);
  //           y = parseInt(value[1], 10);
  //         }
  //         if (this.coordinates.includes(`${npc.x}, ${npc.y}`))
  //           this.npcMove(npc, x, y);
  //         else this.npcMove(npc, x, y, true, false);
  //       } else {
  //         [x, y] = perso.movement;
  //         x = x - this.map_xrange_json[0];
  //         y = y - 4;
  //         npc.move(x, y);
  //       }
  //     }
  //   }
  // }

  npcMove(npc, x, y, arrival = true, depart = true) {
    if (depart) {
      this.currentCor[`${npc.x}, ${npc.y}`] = false;
    }
    npc.move(x, y);
    if (arrival) {
      this.currentCor[`${x}, ${y}`] = true;
    }
  }

  getCoordinates(path) {
    let current = this.map; // 시작은 'map' 객체
    for (const key of path) {
      if (current[key]) {
        current = current[key]; // 다음 단계로 이동
      } else {
        throw new Error(`Path '${key}' not found.`);
      }
    }
    return current;
  }

  getLocJson(loc) {
    // 문자열에서 '@'와 ':' 기호를 기준으로 나누기
    const parts = loc.split("@")[1]; // '@'를 기준으로 나눔
    const [category, ...subParts] = parts.split(":"); // ':'를 기준으로 나눔
    if (subParts[0] == "Gallery") subParts[0] = "prometheus gallery";
    // 결과를 배열로 반환
    return subParts;
  }

  makeVaildMove(x, y) {}
}
//   isupdated(yet = false){
//     let temp = reverie.curr_time;
//     if (this.date != temp && yet) {
//       this.date = temp;
//       return true;
//     }
//     return false;
//   }

//   updateNPCs(dt){
//     if (dt) {
//       for (let npc of _npcs) {
//         let [x, y] = reverie.persona[npc.name].movement;
//         npc.move(x, y);
//       }
//     }
//     return false;
//   }

//   onUpdate(){
//     this.updateNPCs(this.isupdated());
//   }

//   isVaildMove(x, y){
//     const coord = [x, y]
//     function searchCoordinates(obj) {
//       for (let key in obj) {
//         if (Array.isArray(obj[key])) {
//           if (obj[key][0] === coord[0] && obj[key][1] === coord[1]) {
//             return true;
//           }
//         } else if (typeof obj[key] === 'object') {
//           if (searchCoordinates(obj[key])) {
//             return true;
//           }
//         }
//       }
//       return false;
//     }
//   return searchCoordinates(this.map);
//   }
//   }
// }

// // q를 눌렀을 때 실행되는 함수
// App.addOnKeyDown(81, function (player) {
// 	App.httpPostJson(
// 		"http://baculum.i234.me:8509/sendfile/",
// 		{

// 		},
// 		{
//       "filename": "mapping_tree.json",
// 		},
// 		(res) => {
// 			App.sayToAll(`${res}`, 0x000000);
// 			// 요청 결과를 JSON 오브젝트로 변환
// 			let response = JSON.parse(res);
// 			App.sayToAll(`보낸 파일 이름: ${response.data.filename}`, 0x000000);
// 		}
// 	);
// });

// // 플레이어가 입장할 때 동작하는 함수
// App.onJoinPlayer.Add(function (player) {

// });

// let test = null, test2 = null;
// Q를 누르면 동작하는 함수
// App.addOnKeyDown(KeyCodeType.Q, function (player) {
// player.showImageModal("https://oaidalleapiprodscus.blob.core.windows.net/private/org-oHYYF9WByk2KzjlDedbVqQF7/user-HZiqzmmEpn0dsF8RAvHkWQRw/img-Snwwn2B6vDxGhy9Ne98jNRNU.png?st=2024-07-28T09%3A03%3A40Z&se=2024-07-28T11%3A03%3A40Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-07-27T23%3A40%3A22Z&ske=2024-07-28T23%3A40%3A22Z&sks=b&skv=2023-11-03&sig=Q5PtmawIQwCdS7PKREUFR1mEfvIPdSxA4lBJ774lnF8%3D");
// });

// App.addOnKeyDown(87, function (player) {
// test.sayBallon("Hey James, I noticed you're opening up the gallery today. Have you come across any new artworks that caught your eye?");
// });

App.onInit.Add(function () {
  system = new systemGAgent();

  // timeout is required for with http request.
  setTimeout(function () {
    system.reverie = reverie;
    system.map = map;
    delete reverie;
    delete map;
    system.init();
  }, 2000);

  setInterval(() => {
    system.run();
  }, 180000); //180 0000 = 180sec
  
  App.addOnKeyDown(71, function(player) {
    system.run();
  });

});

let currentConversationNPC = null;  // 현재 대화 중인 NPC를 추적하기 위한 변수
let npcConversations = {};  // 각 NPC와의 대화 히스토리를 저장하는 객체
let curTimestamp = Math.floor(Math.random() * (250 - 100 + 1)) + 100; // 100~250 사이의 랜덤 값 설정

App.addOnKeyDown(70, function(player) {
  if (!system || !system.npc_namelist) return;  // 시스템과 NPC 목록이 정의되어 있는지 확인

  // 플레이어의 현재 위치 가져오기
  let playerX = player.tileX;
  let playerY = player.tileY;

  let closestNPC = null;
  let shortestDistance = Infinity;

  // 모든 NPC를 순회하며 가장 가까운 NPC 찾기
  for (let key of system.npc_namelist) {
    const npc = system._npcs[key];
    const distance = system.calculateDistance(playerX, playerY, npc.x, npc.y);

    if (distance < shortestDistance) {
      shortestDistance = distance;
      closestNPC = npc;
    }
  }

  // 가장 가까운 NPC와 대화하기
  if (closestNPC) {
    closestNPC.sayBallon(`안녕하세요, ${player.name}님!`);
    
    // 현재 NPC가 새로운 NPC인지 확인하고, 히스토리 초기화
    if (currentConversationNPC !== closestNPC) {
      currentConversationNPC = closestNPC;  // 현재 대화 중인 NPC 설정
      npcConversations[currentConversationNPC.name] = [];  // 새로운 NPC 대화 히스토리 초기화
      curTimestamp = Math.floor(Math.random() * (250 - 100 + 1)) + 100;
    }
  }
});

// 사용자의 채팅을 감지하여 현재 대화 중인 NPC가 답변하도록 설정
App.onSay.Add(function(player, text) {
  if (currentConversationNPC) {
    // 현재 대화 중인 NPC가 사용자의 입력에 응답 준비
    currentConversationNPC.sayBallon(`Thinking... (Time at ${curTimestamp})`);
    
    // 대화 히스토리에 현재 대화 추가
    npcConversations[currentConversationNPC.name].push({
      player: player.name,
      text: text
    });

    // API를 통해 NPC 응답을 생성
    let npcName = currentConversationNPC.name;
    //let curTimestamp = 200; //npcConversations[npcName].length;  // 대화 히스토리 길이를 사용하여 타임스탬프 설정
    let query = text;

    App.httpGet(
      `http://baculum.i234.me:8509/user_interrupt/?query=${encodeURIComponent(query)}&npc_name=${encodeURIComponent(npcName)}&cur_timestamp=${curTimestamp}`,
      {},
      function(res) {
        try {
          let response = JSON.parse(res);
          let output = response.out;

          // NPC 응답을 히스토리에 추가
          npcConversations[npcName].push({
            npc: npcName,
            text: output
          });

          setTimeout(function() {
            currentConversationNPC.sayBallon(output);
          }, 2000);  // 2초 후에 대답

        } catch (error) {
          App.sayToAll("NPC 응답 생성 중 오류가 발생했습니다.", 0xff0000);
        }
      }
    );
  }
});


// let currentConversationNPC = null; // 현재 대화 중인 NPC를 추적하기 위한 변수
// App.addOnKeyDown(70, function(player){

//   // 플레이어의 현재 위치 가져오기
//   let playerX = player.tileX;
//   let playerY = player.tileY;

//   let closestNPC = null;
//   let shortestDistance = Infinity;

//   // 모든 NPC를 순회하며 가장 가까운 NPC 찾기
//   for (let key of system.npc_namelist) {
//     const npc = system._npcs[key];
//     const distance = system.calculateDistance(playerX, playerY, npc.x, npc.y);

//     if (distance < shortestDistance) {
//       shortestDistance = distance;
//       closestNPC = npc;
//     }
//   }

//   // 가장 가까운 NPC와 대화하기
//   if (closestNPC) {
//     closestNPC.sayBallon(`안녕하세요, ${player.name}님!`);
//     currentConversationNPC = closestNPC; // 현재 대화 중인 NPC 설정
//   }

// })


// // 사용자의 채팅을 감지하여 현재 대화 중인 NPC가 답변하도록 설정
// App.onSay.Add(function(player, text) {
//   if (currentConversationNPC) {
//     // 현재 대화 중인 NPC가 사용자의 입력에 응답
//     currentConversationNPC.sayBallon(`"생각 중이에요...`);
    
//     // API를 통해 NPC 응답을 생성
//     let npcName = currentConversationNPC.name;
//     let curTimestamp = 200; // 현재 타임스탬프 (초 단위)
//     let query = text;

//     App.httpGet(
//       `http://baculum.i234.me:8509/user_interrupt/?query=${encodeURIComponent(query)}&npc_name=${encodeURIComponent(npcName)}&cur_timestamp=${curTimestamp}`,
//       {},
//       function(res) {
//         try {
//           let response = JSON.parse(res);
//           let output = response.out;

//           setTimeout(function() {
//             currentConversationNPC.sayBallon(output);
//           }, 2000); // 2초 후에 대답

//         } catch (error) {
//           App.sayToAll("NPC 응답 생성 중 오류가 발생했습니다.", 0xff0000);
//         }
//       }
//     );
//   }
// });