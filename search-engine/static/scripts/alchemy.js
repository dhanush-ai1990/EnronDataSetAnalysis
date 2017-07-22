var json =  {
    "comment": "Network Graph",
    "nodes": [
        {
            "id": "s1",
            "caption": "Oil",
            "role": "topic",
            "memoryUsage": 50,
            "root": true
        },
        {
            "id": "s2",
            "caption": "Sahba Ezami",
            "role": "person",
            "memoryUsage": 22,
            "root": false
        },        
        {
            "id": "s3",
            "caption": "Aditi Miglani",
            "role": "person",
            "memoryUsage": 95,
            "root": false
        },
        {
            "id": "s4",
            "caption": "Tax",
            "role": "topic",
            "memoryUsage": 10,
            "root": true
        },
        {
            "id": "s5",
            "caption": "Ada Ene",
            "role": "person",
            "memoryUsage": 30,
            "root": false
        },
        {
            "id": "s6",
            "caption": "Dhanush Dharmaretnam",
            "role": "person",
            "memoryUsage": 10, 
            "root": false
        },
        {
            "id": "s7",
            "caption": "Eric Rumfels",
            "role": "person",
            "memoryUsage": 42,
            "root": false
        },
        {
            "id": "s8",
            "caption": "Greg Olmstad",
            "role": "person",
            "memoryUsage": 42,
            "root": false
        },
        {
            "id": "s9",
            "caption": "Finance",
            "role": "topic",
            "memoryUsage": 42,
            "root": true
        },
        {
            "id": "s10",
            "caption": "Oren Kumer",
            "role": "topic",
            "memoryUsage": 42,
            "root": false
        },
        {
            "id": "s11",
            "caption": "Jose Domingo",
            "role": "topic",
            "memoryUsage": 42,
            "root": false
        }

    ],
    "edges": [
        {
            "source": "s1",
            "target": "s2",
            "load": 2
        },
        {
            "source": "s1",
            "target": "s3",
            "load": 2
        },
        {
            "source": "s1",
            "target": "s5",
            "load": 2
        },
        {
            "source": "s1",
            "target": "s6",
            "load": 4
        },
        {
            "source": "s4",
            "target": "s7",
            "load": 1
        },
        {
            "source": "s8",
            "target": "s4",
            "load": 1
        },
        {
            "source": "s8",
            "target": "s9",
            "load": 5
        },
        {
            "source": "s9",
            "target": "s10",
            "load": 1
        },
        {
            "source": "s9",
            "target": "s11",
            "load": 2
        }
    ]
};
      var config = {
            dataSource: json,
            nodeTypes: { "role": 
                ["topic", "person"] 
            }, 
            nodeCaptionsOnByDefault: true,
            forceLocked: false,
            nodeStyle: {
                
                "all": {
                    "borderColor": "#000000",
                    "borderWidth": function(d, radius) {
                        return 5
                    },
                    "color": function(d) { 

                        if(d.getProperties().root)
                        return "#DAA520"; else return "#CD5C5C"
                    }, 
                    "radius": function(d) {
                        if(d.getProperties().root)
                        return 30; else return 12 
                    }, 
                    "text": function(d) {
                        display: block;
                    }, 
                }
            },
            edgeStyle: {
                "all": {
                    "width": function(d) {
                     return (d.getProperties().load + 0.5) * 1.3 
                    }
                }
            }
        };

    alchemy = new Alchemy(config)
