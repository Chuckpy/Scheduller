import React from 'react' 


class ExampleComponent extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            data: 'My name is User'
        };
        console.log(this.state.data)
    };
    
    render() {
      return (
        <div>            
          <h1>{this.state.data}</h1>
        </div>
      );
    }
  }


export default ExampleComponent