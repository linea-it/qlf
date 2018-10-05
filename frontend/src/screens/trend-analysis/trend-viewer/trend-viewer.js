import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';

const apiUrl = process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 215px)',
    width: 'calc(100vw - 280px)',
  },
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    float: 'right',
  },
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
  },
};

class TrendViewer extends React.Component {
  static propTypes = {
    arm: PropTypes.string,
    amp: PropTypes.string,
    plot: PropTypes.string,
    xaxis: PropTypes.string,
    yaxis: PropTypes.string,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
  };

  componentDidMount() {
    document.title = 'Trend Analysis';
    if (window.location.pathname === '/trend-analysis') {
      if (window.location.search.includes('process=')) {
        this.setState({
          processId: window.location.search.split('process=')[1],
        });
      }
    }
  }

  renderImage = () => {
    const { classes } = this.props;
    let url = '';

    if (
      this.props.plot === 'timeseries' &&
      this.props.yaxis !== '' &&
      this.props.amp !== '' &&
      this.props.startDate !== '' &&
      this.props.endDate !== ''
    )
      url = `${apiUrl}dashboard/load_series/?plot=${this.props.plot}&xaxis=${
        this.props.yaxis
      }${this.props.amp}&start=${1}&end=${700}`;
    else if (
      this.props.plot === 'regression' &&
      this.props.xaxis !== '' &&
      this.props.yaxis !== '' &&
      this.props.amp !== '' &&
      this.props.startDate !== '' &&
      this.props.endDate !== ''
    )
      url = `${apiUrl}dashboard/load_series/?plot=${this.props.plot}&xaxis=${
        this.props.xaxis
      }${this.props.amp}&yaxis=${this.props.yaxis}${this.props.amp}`;

    if (url !== '')
      return (
        <iframe
          title="image-modal"
          className={classes.iframe}
          frameBorder="0"
          src={url}
          onLoad={this.props.loadEnd}
        />
      );
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.preview}>
        <FormLabel component="legend">Preview:</FormLabel>
        {this.renderImage()}
      </div>
    );
  }
}

export default withStyles(styles)(TrendViewer);