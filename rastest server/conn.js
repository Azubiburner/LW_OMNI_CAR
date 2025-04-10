const socket = new WebSocket('ws://localhost:8000');
        socket.addEventListener('open', function (event) {
            socket.send('Connection Established');
        });
    
        socket.addEventListener('message', function (event) {
        console.log(event.data);
        });
        
        function move(carId, direction) {
            socket.send(`{${carId},${direction}}`);
            console.log(`{${carId} bewegt sich ${direction}}`);
        }
        function followLine(carId) {
            console.log(`${carId} folgt der Linie`);
            socket.send(`${carId} folgt der Linie`);
        }
        
        
        let selectedCar = null; // Globale Variable für das ausgewählte Auto
    
        // Funktion zum Auswählen eines Autos
        function selectCar(carId) {
            selectedCar = carId;
            console.log(`${carId} wurde ausgewählt`);
            socket.send(`{${carId},ausgewählt}`);
        }
    
        // Funktion zur Steuerung der Bewegungen per Tastatur
        const pressedKeys = new Set();

        document.addEventListener('keydown', (event) => {
            if (!selectedCar) {
                console.log('Kein Auto ausgewählt');
                return;
            }
        
            const key = event.key.toLowerCase();
        
            // Mehrfache Events bei gedrückter Taste verhindern
            if (pressedKeys.has(key)) return;
            pressedKeys.add(key);
        
            switch (key) {
                case 'w':
                    move(selectedCar, 'forward');
                    break;
                case 'a':
                    move(selectedCar, 'left');
                    break;
                case 's':
                    move(selectedCar, 'backward');
                    break;
                case 'd':
                    move(selectedCar, 'right');
                    break;
                case 'q':
                    console.log(`${selectedCar}: Links drehen`);
                    break;
                case 'e':
                    console.log(`${selectedCar}: Rechts drehen`);
                    break;
                default:
                    console.log('Nicht zugeordnete Taste');
            }
        });
        
        document.addEventListener('keyup', (event) => {
            if (!selectedCar) return;
        
            const key = event.key.toLowerCase();
            pressedKeys.delete(key);
        
            switch (key) {
                case 'w':
                case 'a':
                case 's':
                case 'd':
                    move(selectedCar, 'stop');
                    break;
                case 'q':
                case 'e':
                    console.log(`${selectedCar}: Drehung stoppen`);
                    break;
            }
        });
        
       
        