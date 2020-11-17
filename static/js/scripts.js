var url = window.location.origin;

const selectArea = async () => {
    document.getElementById('id_area').addEventListener('change', async (el) => {
        let valueSelected = el.currentTarget.value;
        let response = await fetch(`${url}/areas/${valueSelected}`);

        let json = await response.json();
        let html = `<option value="">---------</option>`;
        let first = true;
        for(let item of json.positions){
            if(first){
                html += `<option value="${item.id}" selected>${item.name}</option>`;
            }else{
                html += `<option value="${item.id}">${item.name}</option>`;
            }
            first = false;
        }
        document.getElementById('id_position').innerHTML = html;

        let selectedPosition = document.getElementsByClassName('form-group--hide')[0].getElementsByTagName('select')[0].value;
        if(selectedPosition === ""){
            console.log(1)
            document.getElementsByClassName('form-group--hide')[0].classList.add('form-group--hide');
        }else{
            console.log(2)
            document.getElementsByClassName('form-group--hide')[0].classList.remove('form-group--hide');
        }
    })
};

window.addEventListener('load', () => {
    selectArea();
    let selectedPosition = document.getElementsByClassName('form-group--hide')[0].getElementsByTagName('select')[0].value;
    if (selectedPosition !== "")  {
        document.getElementsByClassName('form-group--hide')[0].classList.remove('form-group--hide');
    }
});