const API = "http://127.0.0.1:8000";

async function loadVideo(){

    const url = document.getElementById("videoUrl").value;

    const response = await fetch(

        `${API}/load-video`,

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                url:url

            })

        }

    );

    const data = await response.json();

    alert("Video Indexed!");

    console.log(data);

}

async function askQuestion(){

    const question = document.getElementById("question").value;

    const response = await fetch(

        `${API}/ask`,

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                question:question

            })

        }

    );

    const data = await response.json();

    document.getElementById("answer").innerHTML = data.answer;

}