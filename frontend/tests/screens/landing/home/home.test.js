import Home from '../../../../src/screens/landing/widgets/home/home';
import { mount, configure } from 'enzyme';
import React from 'react';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Landing Home', () => {
  let wrapper;
  const updateUrl = jest.fn();

  beforeEach(() => {
    const home = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Home updateUrl={updateUrl} />;
      </MuiThemeProvider>
    );
    wrapper = mount(home);
  });

  afterEach(() => {
    updateUrl.mockReset();
    wrapper.unmount();
  });

  it('has all cads completed', () => {
    expect(
      wrapper
        .find('a')
        .at(0)
        .text()
    ).toBe(
      'Pipeline MonitorwebControl and monitor the execution of the Quick Look pipeline'
    );
    expect(
      wrapper
        .find('a')
        .at(1)
        .text()
    ).toBe(
      'Processing Historyadd_to_queueList exposures that have been processed'
    );
    expect(
      wrapper
        .find('a')
        .at(2)
        .text()
    ).toBe(
      'Observing HistoryhistoryDisplay time series plots for QA metrics, list of exposures and observed targets for the current night of for a range of nights'
    );
    expect(
      wrapper
        .find('a')
        .at(3)
        .text()
    ).toBe(
      'Afternoon Planningbrightness_mediumBrowse QA results for exposures processed by the offline pipeline at NERSC'
    );
    expect(
      wrapper
        .find('a')
        .at(4)
        .text()
    ).toBe(
      'Trend Analysistrending_upSimple plots using quantities stored in the database'
    );
    expect(
      wrapper
        .find('a')
        .at(5)
        .text()
    ).toBe(
      'Observing ConditionscloudDisplay observing conditions such as atmospheric transparency, seeing, and observing background from the GFA camera'
    );
    expect(
      wrapper
        .find('a')
        .at(6)
        .text()
    ).toBe(
      'Survey ReportsassignmentShow the overall progress and performance of survey'
    );
    expect(
      wrapper
        .find('a')
        .at(7)
        .text()
    ).toBe(
      'Configurationview_moduleConfiguration of initial settings for execution'
    );
  });

  it('resizes screen', () => {
    global.innerWidth = 500;
    global.dispatchEvent(new Event('resize'));
  });

  it('navigates to /monitor-realtime', () => {
    wrapper
      .find('a')
      .at(0)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/monitor-realtime');
  });

  it('navigates to /processing-history', () => {
    wrapper
      .find('a')
      .at(1)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/processing-history');
  });

  it('navigates to /observing-history', () => {
    wrapper
      .find('a')
      .at(2)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/observing-history');
  });

  it('navigates to /afternoon-planning', () => {
    wrapper
      .find('a')
      .at(3)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/afternoon-planning');
  });

  it('navigates to /survey-report', () => {
    wrapper
      .find('a')
      .at(6)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/survey-report');
  });

  it('navigates to /', () => {
    wrapper
      .find('a')
      .at(4)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/trend-analysis');
    updateUrl.mockReset();
    wrapper
      .find('a')
      .at(5)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/observing-conditions');
    updateUrl.mockReset();
    wrapper
      .find('a')
      .at(7)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/configuration');
  });
});
