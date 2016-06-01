import React from 'react';
import ReactDOM from 'react-dom';
import Hjs from 'highlight.js';

class Highlight extends React.Component {
    componentDidMount() {
        this._highlightCode();
    }

   componentDidUpdate() {
       this._highlightCode();
   }

    _highlightCode() {
        let node = ReactDOM.findDOMNode(this.refs.code);
        Hjs.highlightBlock(node);
    }

    render() {
        return (
            <pre>
                <code className={this.props.className} ref="code">
                    {this.props.children}
                </code>
            </pre>
        );
    }
};

Highlight.PropTypes = {
    className: React.PropTypes.string
};

export default Highlight;
