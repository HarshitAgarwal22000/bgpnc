<style>
.Logincard
{
    background-color: azure;
    width: 40%;
    height: 50%;
    align-items: center;
    justify-content: center;
    display:flex;
    margin: auto;
    
}
</style>
<script>
    import { debug, tick } from "svelte/internal";

let password;
let username;
let submit;
async function update()
{
    await tick();
    console.log(password.value)
    console.log(username.value)
    

}
async function submitBack()
{
    await tick();
    let passVal=password.value;
    let userVal=username.value;
    let cred={
        Pass:passVal,
        Username:userVal
    }
    
    let response=await fetch ("http://localhost:8000/login",
    {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({cred})
    }
    )
    console.log("Resposne",response);
    let data=await response.json()
    let responsedata=JSON.stringify(data)
    console.log(responsedata)


}

</script>

<div class="Logincard" >
 
    <h3>Login</h3>
    <h4>Username</h4>
    <input bind:this={username} on:input={update}>
    <h5>Password</h5>
    <input bind:this={password} on:input={update}>
    <button bind:this={submit} on:click={submitBack}>Submit</button>
   

</div>
