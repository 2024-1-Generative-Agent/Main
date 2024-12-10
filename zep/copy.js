// let meta = ``;

// meta = JSON.parse(meta);
// console.log(meta.filelist.step_0);
// console.log(move.persona);

// function place_npc() {
//   for (let key in reverie.persona) {
//     let npc = reverie.persona[key];
//     let [x, y] = npc.movement;

//     let npcObj = new buildNPC(key, x, y);
//     _npcs.push(npcObj);
//   }
// }

class buildNPC {
  constructor(name, x, y) {
    if (name) this.name = name;
    else this.name = "NPC";

    if (x) this.x = x;
    else this.x = 0;

    if (y) this.y = y;
    else this.y = 0;

    this.caller = "";

    this.property = {
      key: this.name,
      moveSpeed: 80,
      useDirAnim: true,
      impassable: true,
      collide: true,
      offsetX: -8,
      offsetY: -32,
      oberlap: false,
      npcProperty: { name: this.name },
    };

    this.load_sprite("sprite000.png");

    this.build();
  }

  build() {
    Map.putObjectWithKey(this.x, this.y, this.sprite, {
      overlap: true,
      movespeed: 50,
      key: this.name,
      collide: true,
      useDirAnim: true,
      offsetX: -8,
      offsetY: -32,
      collide: true,
    });

    this.updateProperty();
    this.getLoc();
  }

  load_sprite(spriteName) {
    this.sprite = App.loadSpritesheet(
      spriteName,
      48,
      64,
      {
        left: [5, 6, 7, 8, 9], // 좌방향 이동 이미지
        up: [15, 16, 17, 18, 19],
        down: [0, 1, 2, 3, 4],
        right: [10, 11, 12, 13, 14],
        dance: [
          20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
          37,
        ],
        down_jump: [38],
        left_jump: [39],
        right_jump: [40],
        up_jump: [41],
      },
      10
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

  //   // A* 알고리즘으로 최적 경로 계산
  // function calculatePath(start, end, obstacles) {
  //     // 경로 계산 로직 구현
  //     // ...
  //     // 임시적으로 현재 위치에서 목표 위치로 직선 경로를 반환하는 예시를 작성합니다.
  //     var path = [];
  //     var deltaX = end.x - start.x;
  //     var deltaY = end.y - start.y;
  //     var stepX = deltaX > 0 ? 1 : -1;
  //     var stepY = deltaY > 0 ? 1 : -1;
  //     var x = start.x;
  //     var y = start.y;

  //     while (x !== end.x || y !== end.y) {
  //         if (x !== end.x) {
  //             x += stepX;
  //         }
  //         if (y !== end.y) {
  //             y += stepY;
  //         }
  //         if (!isObstacle(x, y, obstacles)) {
  //             path.push({ x: x, y: y });
  //         } else {
  //             // 장애물이 있는 경우, 이동 중지
  //             break;
  //         }
  //     }

  //     return path;
  // }

  // // 특정 위치가 장애물인지 확인하는 함수
  // isObstacle(x, y) {
  //     let isValid =
  //     Map.getTile(2, x, y) === 0 &&
  // }

  destruct() {
    Map.putObjectWithKey(this.x, this.y, null, { key: this.name });
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

class system {
  constructor() {
    this.api_url = "http://baculum.i234.me:8509";
    this.api_key = "ga-b696fcb5ef00f7921ca69f0447993254" 
    this.httppost();
    // this.httppost(`${this.api_url}/sendfile`, `\"Authorization\" : \"${this.api_key}\"`, `\"filename\" : \"concated_json.json\"`);
    // request persona names to server
    // temp
    // this.sprite_sheet_list = meta.metadata.persona_names;
    // this.date = meta.metadata.curr_time;
    // this.map = meta.metadata.map
    // this._npcs = [];
  }

  httpget(url = "http://baculum.i234.me:8509/", headers = null){
    let response;
    App.httpGet(
      url,
      headers,
      function (res) {
        // 응답 결과를 JSON 오브젝트로 변경
        response = JSON.parse(res);
        App.sayToAll(`받은 데이터 : ${JSON.stringify(res)}`);
        // player.name = response;
        // player.sendUpdated();
      }
    );
    return response
  }

  // httppost(url = "http://baculum.i234.me:8509/", headers = null, body = null){
  httppost(url = "http://baculum.i234.me:8509/", headers = null, body = null){  
    let response;
    App.httpPost(
      "http://baculum.i234.me:8509/sendfile/",
      {Authorization : "user1_api_key"},
      {filename : "concated_json.json"},
      (res) => {
        // 요청 결과를 JSON 오브젝트로 변환
        response = JSON.parse(res);
        App.sayToAll(`받은 데이터 : ${JSON.stringify(res)}`);
        
      }
    );
    return response
  }

  // movement 0.json; place npc on the initial location
  // init() {
  //   for (let key in this.sprite_sheet_list) {
  //     let npc = reverie.persona[key];
  //     let [x, y] = npc.movement;
  //     if (this.isVaildMove(x, y)) {
  //       continue;
  //     }
  //     let npcObj = new buildNPC(key, x, y);
  //     this._npcs.push(npcObj);
  //   }
  // }

  isupdated(yet = false){
    let temp = reverie.curr_time;
    if (this.date != temp && yet) {
      this.date = temp;
      return true;
    }
    return false;
  }

  updateNPCs(dt){
    if (dt) {
      for (let npc of _npcs) {
        let [x, y] = reverie.persona[npc.name].movement;
        npc.move(x, y);
      }
    }
    return false;
  }

  onUpdate(){
    this.updateNPCs(this.isupdated());
  }

  isVaildMove(x, y){
    const coord = [x, y]
    function searchCoordinates(obj) {
      for (let key in obj) {
        if (Array.isArray(obj[key])) {
          if (obj[key][0] === coord[0] && obj[key][1] === coord[1]) {
            return true;
          }
        } else if (typeof obj[key] === 'object') {
          if (searchCoordinates(obj[key])) {
            return true;
          }
        }
      }
      return false;
    }
  return searchCoordinates(this.map);
  }
}

// let test = null, test2 = null;
// Q를 누르면 동작하는 함수
// App.addOnKeyDown(KeyCodeType.Q, function (player) {
  // player.showImageModal("https://oaidalleapiprodscus.blob.core.windows.net/private/org-oHYYF9WByk2KzjlDedbVqQF7/user-HZiqzmmEpn0dsF8RAvHkWQRw/img-Snwwn2B6vDxGhy9Ne98jNRNU.png?st=2024-07-28T09%3A03%3A40Z&se=2024-07-28T11%3A03%3A40Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-07-27T23%3A40%3A22Z&ske=2024-07-28T23%3A40%3A22Z&sks=b&skv=2023-11-03&sig=Q5PtmawIQwCdS7PKREUFR1mEfvIPdSxA4lBJ774lnF8%3D");
// });

// App.addOnKeyDown(87, function (player) {
  // test.sayBallon("Hey James, I noticed you're opening up the gallery today. Have you come across any new artworks that caught your eye?");
// });

//App.onInit.Add(function () {
//  system = new system();
  // system.init();
//});

// App.onInit.Add(function () {
//   //NPC 추가
//   _npcs.push(new buildNPC("테스터", 21, 48));
// });

// App.onSay.add(function (player, text) {
//   //말해보기
//   for (let npc of _npcs) {
//     npc.responseToPlayer(text);
//   }
// });

// App.onUpdate.Add(function (dt) {
//   //위치 얻기
//   for (let npc of _npcs) {
//     npc.getLoc();
//   }
// });

// App.onDestroy.Add(function () {
//   //모든 오브젝트 제거
//   Map.clearAllObjects();
// });
